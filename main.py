import streamlit as st
from authlib.integrations.httpx_client import AsyncOAuth2Client
from pydantic import BaseModel
import httpx
import asyncio
from typing import Optional

# Credentials
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
client = AsyncOAuth2Client(client_id, client_secret, redirect_uri="https://vendor.qlub.cloud/pos/ls-o-series")

# Authorization URL
auth_endpoint = 'https://my.kounta.com/authorize'
token_endpoint = "https://api.kounta.com/v1/token.json"
uri, state = client.create_authorization_url(auth_endpoint)


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: Optional[str] = None
    expires_at: int


def get_payment_method(access_token: str, company_id: str) -> str:
    url = f"https://api.kounta.com/v1/companies/{company_id}/payment_methods.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = httpx.get(url=url, headers=headers)
    for payment_method in r.json():
        if payment_method.get("name") == "Qlub":
            return f"Method Id: {payment_method.get('id')}"
    return "Payment method not found."


async def main():
    st.title("Kounta OAuth2 Dashboard")

    # Step 1: Get Authorization URL
    if st.button("Generate Authorization URL"):
        st.write(f"Authorization URL: [Click here]({uri})")

    # Step 2: Get Tokens
    auth_response = st.text_input("Enter Authorization Response:")
    if st.button("Fetch Tokens"):
        token = await client.fetch_token(token_endpoint, authorization_response=auth_response)
        Ls_token = Token(**token)
        st.session_state.access_token = Ls_token.access_token
        st.write(f"Access Token: {Ls_token.access_token}")
        st.write(f"Refresh Token: {Ls_token.refresh_token}")

    # Step 3: Get Payment Method
    company_id = st.text_input("Enter Company ID:")
    if st.button("Get Payment Method"):
        payment_method_id = get_payment_method(st.session_state.access_token, company_id)
        st.write(payment_method_id)


if __name__ == "__main__":
    asyncio.run(main())

