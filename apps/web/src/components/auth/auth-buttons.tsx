"use client";

import { useAuth, SignInButton, UserButton } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";

export function AuthButtons() {
  const { isSignedIn } = useAuth();

  if (isSignedIn) {
    return <UserButton />;
  }

  return (
    <SignInButton mode="redirect">
      <Button variant="outline" size="sm">
        Sign In
      </Button>
    </SignInButton>
  );
}
