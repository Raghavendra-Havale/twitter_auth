import streamlit as st
from tweepy import OAuthHandler, API

# Twitter API credentials (replace with your keys)
API_KEY = "oBV03LC53HJwAAkgeg5guelNp"
API_SECRET_KEY = "pmi5fKqAipwAjnaNSn8PUdoGPcUpF7UzHuG2zxAziHIYjexo4M"
CALLBACK_URL = "http://localhost:8501"  # Update to your Streamlit deployment URL for production

# Initialize OAuthHandler
auth = OAuthHandler(API_KEY, API_SECRET_KEY, CALLBACK_URL)


def get_authenticated_api():
    """Returns an authenticated Tweepy API instance."""
    if "access_token" in st.session_state and "access_token_secret" in st.session_state:
        auth.set_access_token(st.session_state["access_token"], st.session_state["access_token_secret"])
        return API(auth)
    return None


# Streamlit UI
st.title("Tweet Generator and Poster")
st.markdown("Authenticate with Twitter to post a tweet from your account.")

if "access_token" not in st.session_state:
    # Handle OAuth flow
    if "oauth_verifier" in st.query_params:
        # Handle callback with OAuth verifier
        verifier = st.query_params["oauth_verifier"]
        auth.request_token = {
            "oauth_token": st.session_state["request_token"],
            "oauth_token_secret": st.session_state["request_token_secret"],
        }
        try:
            access_token, access_token_secret = auth.get_access_token(verifier)
            st.session_state["access_token"] = access_token
            st.session_state["access_token_secret"] = access_token_secret
            st.success("Authentication successful!")
        except Exception as e:
            st.error(f"Authentication failed: {e}")
    else:
        # Display login link
        try:
            redirect_url = auth.get_authorization_url()
            st.session_state["request_token"] = auth.request_token["oauth_token"]
            st.session_state["request_token_secret"] = auth.request_token["oauth_token_secret"]
            st.markdown(f"[Login with Twitter]({redirect_url})")
        except Exception as e:
            st.error(f"Error generating login URL: {e}")
else:
    # User is authenticated
    st.success("Authenticated with Twitter!")
    api = get_authenticated_api()

    # Tweet composer
    tweet_content = st.text_area("Compose your Tweet", max_chars=280, placeholder="What's happening?")
    if st.button("Post Tweet"):
        if tweet_content.strip():
            try:
                response = api.update_status(tweet_content)
                st.success(f"Tweet posted successfully! [View Tweet](https://twitter.com/user/status/{response.id})")
            except Exception as e:
                st.error(f"Failed to post tweet: {e}")
        else:
            st.warning("Tweet content cannot be empty!")
