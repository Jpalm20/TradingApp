import React from "react";
import { 
  Flex, 
  Heading, 
  Avatar, 
  Link,
  Text,
  Center,
  ButtonGroup,
  Button,
  Spacer } from "@chakra-ui/react";
import { Link as RouterLink} from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Home from './Home'

export default function Navbar({ user }) {
  const { trade } = useSelector((state) => state.trade);
  
  return (
    <Flex justify="space-between" backgroundColor="teal.600">
      <Heading m={2} color="white">
        MyTradingTracker
      </Heading>
      {((user && Object.keys(user).length > 2) && !(trade && Object.keys(trade).length > 2)) ? (
        <><Spacer /><Center h="65px">
          <ButtonGroup gap='2'>
          <Link as={RouterLink} to="/">
            <Button colorScheme='teal' border='1px' borderColor='black'>
              Home
            </Button>
          </Link>
          <Link as={RouterLink} to="/summary">
            <Button colorScheme='teal' border='1px' borderColor='black'>
              Trades
            </Button>
          </Link>
          <Link as={RouterLink} to="/logTrade">
            <Button colorScheme='teal' border='1px' borderColor='black'>
              Log A Trade
            </Button>
          </Link>
        </ButtonGroup>
          </Center>
        <Link as={RouterLink} to="/profile">
          <Avatar size="md" m={2} />
        </Link></>
      ) : null}
    </Flex>
  );
}
