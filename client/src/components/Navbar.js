import React from "react";
import { Flex, Heading, Avatar, Link } from "@chakra-ui/react";

export default function Navbar({ user }) {
  return (
    <Flex justify="space-between" backgroundColor="teal.600">
      <Heading m={2} color="white">
        Trading App
      </Heading>
      {!!user ? (
        <Link href="/profile">
          <Avatar size="md" m={2} />
        </Link>
      ) : null}
    </Flex>
  );
}
