import { PublicClientApplication } from "@azure/msal-browser";

export const msal = new PublicClientApplication({
  auth: {
    clientId: import.meta.env.VITE_AAD_CLIENT_ID,
    authority: `https://login.microsoftonline.com/${import.meta.env.VITE_AAD_TENANT_ID}`,
    redirectUri: window.location.origin,
  },
  cache: { cacheLocation: "localStorage" },
});

export async function loginAndGetIdToken() {
  const accounts = msal.getAllAccounts();
  if (accounts.length) {
    const result = await msal.acquireTokenSilent({ account: accounts[0], scopes: ["User.Read"] }).catch(() => null);
    return { idToken: result?.idToken, email: accounts[0].username };
  }
  const result = await msal.loginPopup({ scopes: ["User.Read"] });
  return { idToken: result.idToken, email: result.account.username };
}