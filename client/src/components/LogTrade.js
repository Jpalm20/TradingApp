import React, { useState } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { create , reset} from '../store/trade'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import { getTrades } from '../store/auth'
// import { Link } from "react-router-dom";   

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
  ButtonGroup
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function LogTrade({ user }) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trade } = useSelector((state) => state.trade);
  const tradeLogged = ((trade && Object.keys(trade).length > 2) ? (true):(false));

  const [visib, setVisib] = useState(true);

  const user_id = user.user_id;
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
    if (choiceOptions.value === "Shares"){
      setVisib(false);
      setExpiry("");
      setStrike("");
    }else if (choiceOptions.value === "Options"){
      setVisib(true);
      setExpiry("");
      setStrike("");
    }

  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    await dispatch(
      create({
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
  }

  const handleCancel = (e) => {
    e.preventDefault();
    clearFormStates();
    navigate("/");
  }

  const handleAnswerYes = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    clearFormStates();
    navigate("/logTrade");
  }

  const handleAnswerNo = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    clearFormStates();
    navigate("/");
  }

  // grabbing current date to set a max to the birthday input
  const currentDate = new Date();
  let [month, day, year] = currentDate.toLocaleDateString().split("/");
  // input max field must have 08 instead of 8
  month = month.length === 2 ? month : "0" + month;
  day = day.length === 2 ? day : "0" + day;
  const maxDate = year + "-" + month + "-" + day;

  return (
    <Flex
      flexDirection="column"
      width="100wh"
      height="100vh"
      backgroundColor="gray.200"
      justifyContent="center"
      alignItems="center"
    >
      {!tradeLogged ? (
      <Stack
        flexDir="column"
        mb="2"
        justifyContent="center"
        alignItems="center"
      >
        <Heading color="teal.400">Log A Trade</Heading>
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
                  <Select placeholder='Select Trade Type' onChange={(e) => setTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select id="optionsSelection" placeholder='Select Security Type' onChange={(e) => {changeShowOptions(e.target.value); setSecurityType(e.target.value)}}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" onChange={(e) => setTickerName(e.target.value)} />
                </FormControl>
              </Box>
              
              <Box style={{display: visib ? "flex" : "none"}}>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Expiry (Options Only) *
                </FormHelperText>
                <Input
                    type="date"
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
                    onChange={(e) => setBuyValue(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    # of Units *
                  </FormHelperText>
                  <Input
                    type="name"
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
                    onChange={(e) => setRR(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    PNL *
                  </FormHelperText>
                  <Input
                    type="name"
                    onChange={(e) => setPNL(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    % Win or Loss *
                  </FormHelperText>
                  <Input
                    type="name"
                    onChange={(e) => setPercentWL(e.target.value)}
                  />
              </FormControl>
              </Box>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Comments *
                  </FormHelperText>
                  <Textarea placeholder='Reflect on your Trade...' onChange={(e) => setComments(e.target.value)}/>
              </FormControl>

              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleSubmit}
              >
                Create Trade Entry
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
      ) : (
      <Stack
        flexDir="column"
        mb="2"
        justifyContent="center"
        alignItems="center"
        spacing={4}
        p="1rem"
        backgroundColor="whiteAlpha.900"
        boxShadow="md"
      >
          <Text fontSize='lg' as='b'>
            <Center color="teal.400" >
              Trade Logged Successfully<br></br>Would You Like to Log Another?
            </Center>
          </Text>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleAnswerYes}
              >
                Yes
              </Button>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleAnswerNo}
              >
                No
              </Button>
      </Stack>
      )}
    </Flex>
  );
}
