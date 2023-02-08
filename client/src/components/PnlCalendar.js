import React, { useEffect, useState, Component } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getPnlByYear } from '../store/auth';
import { Link as RouterLink, useNavigate} from "react-router-dom";
import monthsString from "../data/months";

import {
  Flex,
  Center,
  Text,
  HStack,
  VStack,
  Heading,
  Input,
  Button,
  Stack,
  StackDivider,
  Select,
  chakra,
  Box,
  Grid,
  GridItem,
  FormControl,
  FormHelperText,
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { RiCheckboxBlankFill } from "react-icons/ri";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function PnlCalendar({ user }) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { pnlYTD } = useSelector((state) => state.auth);
  const hasPnLInfo = ((pnlYTD && Object.keys(pnlYTD).length > 0 && pnlYTD.months && Object.keys(pnlYTD.months).length > 0) ? (true):(false));

  const [toggleFilter, setToggleFilter] = useState(false);

  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();

  const [calMonth, setCalMonth] = useState(month);
  const [calYear, setCalYear] = useState(year);

  const user_id = user.user_id;

  const [filter_trade_type, setFilterTradeType] = useState("");
  const [filter_security_type, setFilterSecurityType] = useState("");
  const [filter_ticker_name, setFilterTickerName] = useState("");


  var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  });

  var percent = new Intl.NumberFormat('default', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const colorChange = (pnl) => {
    let bgColor;
    if (pnl > 0){
      bgColor = "green.200"
    } else if (pnl < 0) {
      bgColor = "red.200"
    } else {
      bgColor = "gray.200"
    }
    return bgColor;
  };

  const getDays = (yearr, monthh) => {
    return new Date(yearr, monthh, 0).getDate();
  };

  const getBlanksForFirstDay = () => {
    let content = [];
    let firstDay = new Date(calYear, calMonth, 1).getDay();
    for (let i = 0; i < firstDay; i++) {
      content.push(<GridItem w='100%' h='100%' bg='gray.200' >
                  -
                  <Center fontWeight='bold' >
                    -
                  </Center>
                </GridItem>);
    }
    return content;
  };

    const getBlanksForEndOfMonth = () => {
    let content = [];
    let totalDays = getDays(calYear, calMonth);
    let firstDay = new Date(calYear, calMonth, 1).getDay();
    let spotsLeft = 42-totalDays-1-firstDay;
    for (let i = 0; i < spotsLeft; i++) {
      content.push(<GridItem w='100%' h='100%' bg='gray.200' >
                  -
                  <Center fontWeight='bold' >
                    -
                  </Center>
                </GridItem>);
    }
    return content;
  };

  const getMonthlyTotal = () => {
    let monthlyTotal = 0;
    for (let i = 0; i < 31; i++) {
      monthlyTotal += pnlYTD.months[calMonth][calMonth][i]
    }
    return monthlyTotal;
  };

  const getGreenDayTotal = () => {
    let greenDayTotal = 0;
    for (let i = 0; i < 31; i++) {
      if(pnlYTD.months[calMonth][calMonth][i] > 0){
        greenDayTotal += 1
      }
    }
    return greenDayTotal;
  };

  const getRedDayTotal = () => {
    let redDayTotal = 0;
    for (let i = 0; i < 31; i++) {
      if(pnlYTD.months[calMonth][calMonth][i] < 0){
        redDayTotal += 1
      }
    }
    return redDayTotal;
  };

  const getGreenDayPercent = () => {
    let greenDays = 0;
    let totalDays = getDays(calYear, calMonth);
    for (let i = 0; i < totalDays; i++) {
      if(pnlYTD.months[calMonth][calMonth][i] > 0){
        greenDays += 1
      }
    }
    return ((greenDays/totalDays));
  };

  const getWeeklyTotals = () => {
    let content = [];
    let weekTotals = [0.0,0.0,0.0,0.0,0.0,0.0];
    let weekCount = 0;
    let dayCount = 0;
    let pnlDayCount = 0;
    let firstDay = new Date(calYear, calMonth, 1).getDay();
    while (weekCount <= 6) {
      if(dayCount !== 0 && dayCount%7 === 0){
        weekCount += 1;
      }
      if (weekCount === 0 && dayCount === 0 && firstDay !== 0) {
        dayCount += firstDay;
      }
      if(pnlYTD.months[calMonth][calMonth][pnlDayCount] !== 0.0 && pnlDayCount < 31){
        weekTotals[weekCount] += pnlYTD.months[calMonth][calMonth][pnlDayCount];
      }
      dayCount += 1;
      pnlDayCount += 1;
    }
    for (let i = 0; i < weekTotals.length; i++) {
      content.push(<GridItem w='100%' h='100%' bg={colorChange(weekTotals[i])} >
                  -
                  <Center fontWeight='bold' isNumeric>
                    {formatter.format(weekTotals[i])}
                  </Center>
                </GridItem>);
    }
    return content;
  };

  const getPnlDays = () => {
    let content = pnlYTD.months[calMonth][calMonth].map((pnl, index) => ( 
      <GridItem key={index} w='100%' h='100%' bg={colorChange(pnl)}>
        {index+1}
        <Center fontWeight='bold' isNumeric>
          {formatter.format(pnl)}
        </Center>
      </GridItem>
    ));
    return content;
  }

  useEffect(() => {
    let year = calYear;
    dispatch(getPnlByYear({ user_id, year }));
  }, [calYear]); 

  const handleSubmitFilter = (e) => {
    e.preventDefault();
    setToggleFilter(!toggleFilter);
  }
       

  return (
      
      <Flex           
        flexDirection="column"
        height="100vh"
        backgroundColor="gray.200"
      >
        <Stack
                p="1rem"
                backgroundColor="whiteAlpha.900"
                align='center'
                rounded="lg"
                borderWidth="1px"
              >
        <Heading color="teal.400" w='full'>
          <Center>
            Profit/Loss Calendar
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
                minWidth="30vh"
              >
                <Heading color="teal.400" size="md">Filters</Heading>
                <Box width="full">
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
                  <Button colorScheme='teal' width="full" border='1px' borderColor='black' onClick={handleSubmitFilter} >
                    Submit Filter
                  </Button>
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
            {{hasPnLInfo} ? (
              /*
            <div>
              <Text>
                {pnlYTD.months}
              </Text>
            </div>
            */
            <VStack
              divider={<StackDivider borderColor='gray.200' />}
              spacing={4}
              align='center'
            >
              <HStack align='center'>
                <Select w='75%' size="lg" variant='filled' placeholder={monthsString[calMonth]} onChange={(e) => setCalMonth(monthsString.indexOf(e.target.value))}>
                  {monthsString.map((mmonth) => (<option key={mmonth}>{mmonth}</option>))}
                </Select>
                <Select 
                w='50%' 
                size="lg" 
                variant='filled' 
                placeholder={calYear} 
                onChange={(e) => {
                  setCalYear(e.target.value); 
                }}>
                  <option>{year}</option>
                  <option>{year-1}</option>
                  <option>{year-2}</option>
                  <option>{year-3}</option>
                  <option>{year-4}</option>
                  <option>{year-5}</option>
                  <option>{year-6}</option>
                  <option>{year-7}</option>
                  <option>{year-8}</option>
                  <option>{year-9}</option>
                  <option>{year-10}</option>
                  <option>{year-11}</option>
                  <option>{year-12}</option>
                  <option>{year-13}</option>
                  <option>{year-14}</option>
                  <option>{year-15}</option>
                </Select>
              </HStack>
              <HStack spacing={8}>
              <VStack
                divider={<StackDivider borderColor='gray.200' />}
                spacing={4}
                align='stretch'
              >
              <Grid templateColumns='repeat(7, 1fr)' gap={3}>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Sunday
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Monday
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Tuesday
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Wednesday
                  </Center>
                </GridItem>                
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Thursday
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Friday
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Saturday
                  </Center>
                </GridItem>

              </Grid>
              <Grid templateColumns='repeat(7, 1fr)' templateRows='repeat(6, 1fr)' gap={3}>
                {getBlanksForFirstDay()}
                {getPnlDays()}
                {getBlanksForEndOfMonth()}
              </Grid>
              </VStack>
              <VStack
                divider={<StackDivider borderColor='gray.200' />}
                spacing={4}
                align='stretch'
                display='flex'
              >
              <Grid templateColumns='repeat(1, 1fr)' templateRows='repeat(1, 1fr)' gap={3}>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Weekly Totals
                  </Center>
                </GridItem>
              </Grid>
              <Grid templateColumns='repeat(1, 1fr)' templateRows='repeat(6, 1fr)' gap={3}>
                {getWeeklyTotals()}
              </Grid>
              </VStack>
              </HStack>
              <Grid templateColumns='repeat(4, 1fr)' gap={10}>
                <GridItem w='100%' h='100%' bg={colorChange(getMonthlyTotal())} >
                  <Center fontWeight='bold'>
                    Monthly PnL: {formatter.format(getMonthlyTotal())}
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Green Days: {getGreenDayTotal()}
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    Red Days: {getRedDayTotal()}
                  </Center>
                </GridItem>
                <GridItem w='100%' h='100%' bg='gray.200' >
                  <Center fontWeight='bold'>
                    % Green Days: {percent.format(getGreenDayPercent())}
                  </Center>
                </GridItem>
              </Grid>
            </VStack>
            ) : (
              <Text>
              No PnL Info
              </Text>
            )}

            </Stack>
          </Box>
          </Stack>
        </Flex>
      </Flex>
  )
}

