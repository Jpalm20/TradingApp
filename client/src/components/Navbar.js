import React from "react";
import { getPnlByYear } from '../store/auth'
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

export default function Navbar({ user }) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trade } = useSelector((state) => state.trade);
  const today = new Date();
  const year = today.getFullYear();
  const handleHome = (e) => {
    navigate("/");
  }

  const handlePnlCalendar = async (e, user_id) => {
    await dispatch(getPnlByYear({ user_id, year }));
    navigate("/PnlCalendar");
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
            <Button backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handlePnlCalendar(e.target.value, user.user_id)}>
              Pnl Calendar
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
