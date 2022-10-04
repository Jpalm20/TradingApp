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
  Spacer, 
  Icon} from "@chakra-ui/react";
import { Link as RouterLink, useNavigate} from "react-router-dom";
import { RiStockFill } from "react-icons/ri";
import { useSelector, useDispatch } from "react-redux";
import Home from './Home'

export default function Navbar({ user }) {
  const navigate = useNavigate();
  const { trade } = useSelector((state) => state.trade);

  const handleHome = (e) => {
    navigate("/");
  }

  const handleTrades = (e) => {
    navigate("/summary");
  }

  const handleLogTrade = (e) => {
    navigate("/logTrade");
  }
  
  return (
    <Flex justify="space-between" backgroundColor="teal.600">
      <Heading m={2} color="white">
        MyTradingTracker
        <Icon as={RiStockFill}></Icon>
      </Heading>
      {((user && Object.keys(user).length > 2) && !(trade && Object.keys(trade).length > 2)) ? (
        <><Spacer /><Center h="65px">
          <ButtonGroup gap='2'>
            <Button backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handleHome(e.target.value)}>
              Home
            </Button>
            <Button backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handleTrades(e.target.value)}>
              Trades
            </Button>
            <Button backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handleLogTrade(e.target.value)}>
              Log A Trade
            </Button>
        </ButtonGroup>
          </Center>
        <Link as={RouterLink} to="/profile">
          <Avatar border='1px' borderColor='black' size="md" m={2} />
        </Link></>
      ) : null}
    </Flex>
  );
}
