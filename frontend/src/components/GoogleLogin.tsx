import { useGoogleLogin } from "@react-oauth/google";
import { useState } from "react";
interface GoogleAuthResponse {
  email: string;
  email_verified: boolean;
  family_name: string;
  given_name: string;
  name: string;
  picture: string;
  sub: string;
}

export function GoogleLogin() {
  const [userData, setUserData] = useState<GoogleAuthResponse | null>(null);
  const login = useGoogleLogin({
    flow: "auth-code",
    onSuccess: async (codeResponse) => {
      console.log("Auth Code:", codeResponse.code);
      console.log({ codeResponse });
      try {
        const response = await fetch(`/auth/google`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ code: codeResponse.code }),
        });
        const data = (await response.json()) as GoogleAuthResponse;
        console.log({ data });
        setUserData(data);
      } catch (error) {
        console.log(error);
      }
    },
    onError: (error) => console.log("Login Failed:", error),
  });
  if (userData)
    return (
      <div>
        <div>{userData.name}</div>
        <div>{userData.email}</div>
        <div>
          <img src={userData.picture} alt={userData.name} />
        </div>
      </div>
    );
  return <button onClick={() => login()}>Sign in with Google (Code Flow)</button>;
}
