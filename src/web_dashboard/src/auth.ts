import NextAuth from "next-auth";
import Discord from "next-auth/providers/discord";

export const { handlers, signIn, signOut, auth } = NextAuth({

  providers: [
    Discord,
  ],
  session: {
    strategy: "jwt",
  },
  // ill attempt to explain this
  callbacks: {
    //this callback is only called once, when the user first signs in, so we can inject the access token to the jwt
    jwt({ token, account }) {
      if (account) {
        return {
          ...token,
          access_token: account.access_token as string
        }
      }
      return token
    },
    // anytime auth() (server-side) or useSession (client-side) is called, this is what is returned, 
    // so we can inject the access token from the jwt into the session object
    session({ session, token }) {
      session.access_token = token.access_token
      return session
    }
  },
  secret: process.env.AUTH_SECRET,
  trustHost: true
});
