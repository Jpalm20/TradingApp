import React, { useEffect, useState } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades } from '../store/auth'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import {
  Flex,
  Text,
  Center,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  Textarea,
  Select,
  chakra,
  Box,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
  ButtonGroup,
  Badge,
  HStack
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { update, getTrade, reset } from '../store/trade';

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Summary({ user }) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trade } = useSelector((state) => state.trade);
  const { trades } = useSelector((state) => state.auth);
  const hasTrades = ((trades.trades && Object.keys(trades.trades).length > 3) ? (true):(false));
  const hasTrade = ((trade && Object.keys(trade).length > 2) ? (true):(false));

  const [editTrade, setEditTrade] = useState(false);
  const [toggleFilter, setToggleFilter] = useState(false);

  const [visib, setVisib] = useState(false);
  function checkVisbility(tradePayload){
    setVisib(tradePayload.security_type === "Options");
  }

  const user_id = user.user_id;

  const [trade_id, setTradeID] = useState(null);

  const [trade_type, setTradeType] = useState("");
  const [security_type, setSecurityType] = useState("");
  const [ticker_name, setTickerName] = useState("");
  const [expiry, setExpiry] = useState("");
  const [strike, setStrike] = useState("");
  const [buy_value, setBuyValue] = useState("");
  const [units, setUnits] = useState("");
  const [rr, setRR] = useState("");
  const [pnl, setPNL] = useState("");
  const [percent_wl, setPercentWL] = useState("");
  const [comments, setComments] = useState("");

  const [filter_trade_type, setFilterTradeType] = useState("");
  const [filter_security_type, setFilterSecurityType] = useState("");
  const [filter_ticker_name, setFilterTickerName] = useState("");
  

  function clearFormStates() {
    setTradeType("");
    setSecurityType("");
    setTickerName("");
    setExpiry("");
    setStrike("");
    setBuyValue("");
    setUnits("");
    setRR("");
    setPNL("");
    setPercentWL("");
    setComments("");
  }
  
  const changeShowOptions = (e) => {
    const choiceOptions = document.getElementById("optionsSelection");
    console.log(choiceOptions.value);
    if (choiceOptions.value === "Shares"){
      setVisib(false);
      setExpiry("");
      setStrike("");
    }else if (choiceOptions.value === "Options"){
      setVisib(true);
      setExpiry("");
      setStrike("");
    }
    if (choiceOptions.value === "" && trade.security_type === "Options"){
      setVisib(true);
      setExpiry("");
      setStrike("");
    }else if (choiceOptions.value === "" && trade.security_type === "Shares"){
      setVisib(false);
      setExpiry("");
      setStrike("");
    }
  }

  const handleGotoEdit = async (e, trade_id) => {
    e.preventDefault();
    const res = await dispatch(
      getTrade({
        trade_id
      })
    );
    checkVisbility(res.payload);
    setTradeID(trade_id);
    setEditTrade(true);
  };
  


  const handleDoneEdit = async (e) => {
    e.preventDefault();
    await dispatch(
        update({
          trade_id,
          user_id,
          trade_type,
          security_type,
          ticker_name,
          expiry,
          strike,
          buy_value,
          units,
          rr,
          pnl,
          percent_wl,
          comments
        })
      );
    await dispatch(
      getTrades({
        user_id
      })
    );
    dispatch(
      reset()      
    );
    clearFormStates();
    setEditTrade(false);
  };

  const handleCancel = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    clearFormStates();
    setEditTrade(false);
  }

  const handleSubmitFilter = (e) => {
    e.preventDefault();
    setToggleFilter(!toggleFilter);
  }

  // grabbing current date to set a max to the birthday input
  const currentDate = new Date();
  let [month, day, year] = currentDate.toLocaleDateString().split("/");
  // input max field must have 08 instead of 8
  month = month.length === 2 ? month : "0" + month;
  day = day.length === 2 ? day : "0" + day;
  const maxDate = year + "-" + month + "-" + day;        

  return (
    !editTrade ? (
      <Flex           
        flexDirection="column"
        height="100vh"
        backgroundColor="gray.200"
      >
        <Stack
                p="1rem"
                backgroundColor="whiteAlpha.900"
                boxShadow="md"
                align='center'
                rounded="lg"
              >
        <Heading color="teal.400" w='full'>
          <Center>
            Trade Summary
          </Center>
        </Heading>
        </Stack>

       
        
        <Flex
          w='full'
          flexDirection="row"
          flex="auto"
          backgroundColor="gray.200"
        >
          <Stack
            flexDir="column"
            mb="2"
            justifyContent="left"
            alignItems="center"
          >
            <Box flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch">
              <Stack
                spacing={4}
                p="1rem"
                backgroundColor="whiteAlpha.900"
                boxShadow="md"
                align='center'
              >
                <Heading color="teal.400">Filters</Heading>
                <Box >
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select placeholder='Select Trade Type' onChange={(e) => setFilterTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select placeholder='Select Security Type' onChange={(e) => setFilterSecurityType(e.target.value)}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" placeholder='Enter Ticker' onChange={(e) => setFilterTickerName(e.target.value)} />
                </FormControl>
              </Box>
              <Link as={RouterLink} to="/">
                  <Button colorScheme='teal' width="full" border='1px' borderColor='black' onClick={handleSubmitFilter} >
                    Submit Filter
                  </Button>
              </Link>
              </Stack>
            </Box>
          </Stack>
         
          
          <Stack
            flexDir="column"
            flex="auto"
            mb="2"
          >
          
          <Box flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch">
            <Stack
              flex="auto"
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
              h="full"
              w="full"
              justifyContent="left"
            >
              <Box borderWidth="1px" rounded="lg" overflow="hidden" display="flex" gap='0.5' align='stretch'>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Trade ID
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Trade Type
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Security Type
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Ticker Name
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Expiry
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Strike
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Avg Price
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    # of Units
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    Risk/Reward
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    PNL
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' color="teal.400" align='center'>
                  <Center h='40px'>
                    % W/L
                  </Center>
                </Badge>
                <Badge width='100%' flexGrow="1" variant='outline' borderRadius='12' backgroundColor="grey" color="black" align='center'>
                  <Center h='40px'>
                    
                  </Center>
                </Badge>
              </Box>
              {hasTrades} ? (
                <div>
                {trades.trades.map((trades, index) => (
                  <Box borderWidth="1px" rounded="lg" overflow="hidden" display="flex" gap='0.5' align='stretch' key={index}>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.trade_id}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.trade_type}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.security_type}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.ticker_name}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.expiry}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.strike}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.buy_value}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.units}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.rr}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.pnl}
                    </Center>
                  </Badge>
                  <Badge width='100%' flexGrow="1" borderRadius='12' color="teal.400" align='center'>
                    <Center h='40px'>
                      {trades.percent_wl}
                    </Center>
                  </Badge>
                  <Link as={RouterLink} to="/">
                    <Button width='100px' colorScheme='teal' border='1px' borderColor='black' onClick={e => handleGotoEdit(e, trades.trade_id)}>
                      Edit Trade
                    </Button>
                  </Link>
                  </Box>
                ))}
                </div>
              ) : (

              )
              
            </Stack>
          </Box>
          </Stack>
        </Flex>
      </Flex>
    ) : (
      <Flex
        flexDirection="column"
        width="100wh"
        height="100vh"
        backgroundColor="gray.200"
        justifyContent="center"
        alignItems="center"
      >
        <Stack
          flexDir="column"
          mb="2"
          justifyContent="center"
          alignItems="center"
        >
        <Heading color="teal.400">Update Trade</Heading>
        <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden">
          <form>
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
            >
              <Box display="flex">
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select placeholder={trade.trade_type} onChange={(e) => setTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select id="optionsSelection" placeholder={trade.security_type} onChange={(e) => {changeShowOptions(e.target.value); setSecurityType(e.target.value);}}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" placeholder={trade.ticker_name} onChange={(e) => setTickerName(e.target.value)} />
                </FormControl>
              </Box>
              
              <Box style={{display: visib ? "flex" : "none"}}>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Expiry (Options Only) *
                </FormHelperText>
                <Input
                    placeholder={trade.expiry}
                    onFocus={(e) => (e.target.type = "date")}
                    onBlur={(e) => (e.target.type = "text")}
                    max={maxDate}
                    min="1900-01-01"
                    onChange={(e) => setExpiry(e.target.value)}
                />
              </FormControl>

              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Strike Price (Options Only) *
                </FormHelperText>
                <InputGroup>
                  <Input
                    type="name"
                    placeholder={trade.strike}
                    onChange={(e) => setStrike(e.target.value)}
                  />
                </InputGroup>
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Average Cost *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={trade.buy_value}
                    onChange={(e) => setBuyValue(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    # of Units *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={trade.units}
                    onChange={(e) => setUnits(e.target.value)}
                  />
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Risk/Reward Ratio *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={trade.rr}
                    onChange={(e) => setRR(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    PNL *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={trade.pnl}
                    onChange={(e) => setPNL(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    % Win or Loss *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={trade.percent_wl}
                    onChange={(e) => setPercentWL(e.target.value)}
                  />
              </FormControl>
              </Box>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Comments *
                  </FormHelperText>
                  <Textarea placeholder={trade.comments} onChange={(e) => setComments(e.target.value)}/>
              </FormControl>

              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleDoneEdit}
              >
                Update Trade
              </Button>

              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleCancel}
              >
                Cancel
              </Button>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Flex>
    ) 
  )
}
