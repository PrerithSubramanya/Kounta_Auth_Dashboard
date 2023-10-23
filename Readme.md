# Kounta OAuth2 Dashboard

An interactive Streamlit dashboard that facilitates the OAuth2 authorization process for Kounta's API and subsequently retrieves payment methods associated with a company ID.

## Features

1. **Generate Authorization URL**: Get the OAuth2 authorization URL to authorize the application.
2. **Fetch Tokens**: After authorizing the application from the provided URL, input the authorization response to obtain access and refresh tokens.
3. **Retrieve Payment Methods**: Using the fetched access token, input a company ID to retrieve associated payment methods.
