import React, { useEffect, useState, Component } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades, getTradesFiltered } from '../store/auth'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { Chart } from "react-google-charts";
import { BsFilter } from "react-icons/bs";
import '../styles/filter.css';
import '../styles/home.css';
import {
  Flex,
  Text,
  Switch,
  Center,
  Heading,
  StackDivider,
  Input,
  Grid,
  GridItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  StatGroup,
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
  List,
  ListItem,
  ListIcon,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  Textarea,
  Icon,
  Select,
  chakra,
  Box,
  Link,
  Avatar,
  Spinner,
  Toast,
  useToast,
  FormControl,
  FormHelperText,
  InputRightElement,
  ButtonGroup,
  Badge,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  HStack,
  SimpleGrid,
  FormLabel,
  VStack
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { RiCheckboxBlankFill } from "react-icons/ri";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);


export default function Home({ user }) {
  ChartJS.register(ArcElement, Tooltip, Legend);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef()
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trades } = useSelector((state) => state.auth);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const hasTrades = ((trades.trades && Object.keys(trades.trades).length > 0 && trades.stats && Object.keys(trades.stats).length > 0) ? (true):(false)); //need to look into this for home error
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false));

  const [toggleFilter, setToggleFilter] = useState(false);

  const user_id = user.user_id;

  const [trade_id, setTradeID] = useState(null);

  const [filter_trade_type, setFilterTradeType] = useState("");
  const [filter_security_type, setFilterSecurityType] = useState("");
  const [filter_ticker_name, setFilterTickerName] = useState("");
  const [filter_switch_time, setFilterSwitchDate] = useState("");

  const authLoading = useSelector((state) => state.auth.loading);


  var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  });

  var percent = new Intl.NumberFormat('default', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const pieOptionsA = {
    title: "Day Trade vs Swing Trade",
    chartArea: {
      width: "80%",
      height: "75%"
    },
    height: "100%",
    width: "100%",
    backgroundColor: "#FDFDFD",
    titleTextStyle: {
      color: '#636363',
      fontName: 'Open Sans',
      bold: true,
      fontSize: 18,
    },
    is3D: false,
    pieSliceTextStyle: {
      color: 'black',
    },
    slices: [
      {
        color: "#FF8B8B"
      },
      {
        color: "#F51313"
      },
      {
        color: "#85F98B"
      },
      {
        color: "#017209"
      }
    ],
    legend: {
      position: "left",
    },
  };

  const pieOptionsB = {
    title: "Options vs Shares",
    chartArea: {
      width: "80%",
      height: "75%"
    },
    height: "100%",
    width: "100%",
    backgroundColor: "#FDFDFD",
    titleTextStyle: {
      color: '#636363',
      fontName: 'Open Sans',
      bold: true,
      fontSize: 18,
    },
    is3D: false,
    pieSliceTextStyle: {
      color: 'black',
    },
    slices: [
      {
        color: "#FF8B8B"
      },
      {
        color: "#F51313"
      },
      {
        color: "#85F98B"
      },
      {
        color: "#017209"
      }
    ],
    legend: {
      position: "left",
    },
  };

  const colorChange = (pnl) => {
    let bgColor;
    if (pnl > 0){
      bgColor = "green.400"
    } else if (pnl < 0) {
      bgColor = "red.400"
    } else {
      bgColor = "black"
    }
    return bgColor;
  };

  const pnlValue = (pnl) => {
    if (pnl.includes("-")){
      return "(".concat(pnl.substring(1),")")
    } else {
      return pnl
    }
  };

  const getFilterComponent = () => {
    let content = [];
    content.push(
      <div class="large-component">
            <Box flexGrow="1" display="flex" borderWidth="1px" h="100%" rounded="lg" overflow="hidden" alignItems="stretch">
              <Stack
                spacing={4}
                p="1rem"
                backgroundColor="whiteAlpha.900"
                boxShadow="md"
                align='center'
                minWidth="30vh"
              >
                <Heading class="filterheader">Filters</Heading>
                <Box width="full">
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select placeholder='Select Trade Type' value={filter_trade_type} onChange={(e) => setFilterTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select placeholder='Select Security Type' value={filter_security_type} onChange={(e) => setFilterSecurityType(e.target.value)}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" placeholder='Enter Ticker' value={filter_ticker_name} onChange={(e) => setFilterTickerName(e.target.value)} />
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Time Frame
                  </FormHelperText>
                  <Select placeholder='Select Time Frame' value={filter_switch_time} onChange={(e) => setFilterSwitchDate(e.target.value)}>
                    <option>Year</option>
                    <option>Month</option>
                    <option>Week</option>
                    <option>Day</option>
                  </Select>
                </FormControl>

              </Box>
                  <Button size="sm" backgroundColor='gray.300' width="full" onClick={handleSubmitFilter} >
                    Submit Filter
                  </Button>
                  <Button size="sm" colorScheme='red' width="full" onClick={handleClearFilter} >
                    Clear Filter
                  </Button>
              </Stack>
            </Box>
          </div>
    );
    content.push(
      <div padd class="small-component">
      <Box flexGrow="1"  backgroundColor="whiteAlpha.900" display="flex" borderWidth="1px" h="100%" rounded="lg" overflow="hidden" alignItems="stretch">
      <Button ref={btnRef} colorScheme='white' onClick={onOpen}>
       <Icon as={BsFilter} color='grey' size='lg'></Icon>
      </Button>
      </Box>
      <Drawer
        isOpen={isOpen}
        placement='left'
        onClose={onClose}
        finalFocusRef={btnRef}
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader class="filterheader">Filters</DrawerHeader>

          <DrawerBody>
          <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select placeholder='Select Trade Type' value={filter_trade_type} onChange={(e) => setFilterTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select placeholder='Select Security Type' value={filter_security_type} onChange={(e) => setFilterSecurityType(e.target.value)}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" placeholder='Enter Ticker' value={filter_ticker_name} onChange={(e) => setFilterTickerName(e.target.value)} />
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Time Frame
                  </FormHelperText>
                  <Select placeholder='Select Time Frame' value={filter_switch_time} onChange={(e) => setFilterSwitchDate(e.target.value)}>
                    <option>Year</option>
                    <option>Month</option>
                    <option>Week</option>
                    <option>Day</option>
                  </Select>
                </FormControl>
          </DrawerBody>

          <DrawerFooter>
            <Button size="sm" backgroundColor='gray.300' width="full" onClick={handleSubmitFilter}>
              Submit Filter
            </Button>
            <Button size="sm" colorScheme='red' width="full" onClick={handleClearFilter} >
              Clear Filter
            </Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </div>
    );
    return content
  };


  const handleSubmitFilter = async (e) => {
    e.preventDefault();
    onClose();
    const filters = {};
    if(filter_trade_type !== ''){
      filters.trade_type = filter_trade_type;
    }
    if(filter_security_type !== ''){
      filters.security_type = filter_security_type;
    }
    if(filter_ticker_name !== ''){
      filters.ticker_name = filter_ticker_name;
    }
    if(filter_switch_time !== ''){
      filters.date_range = filter_switch_time;
    }
    await dispatch(
      getTradesFiltered({
        filters,
        user_id
      })
    );
    //setToggleFilter(!toggleFilter);
  }

  const handleClearFilter = async (e) => {
    e.preventDefault();
    onClose();
    setFilterTradeType('');
    setFilterSecurityType('');
    setFilterTickerName('');
    setFilterSwitchDate('');
    await dispatch(
      getTrades({
        user_id
      })
    );
    //setToggleFilter(!toggleFilter);
  }

  useEffect(() => {
    evaluateError();
  }, [error]); 

  const evaluateError = () => {
    if(error === true){
      setToastErrorMessage(info.response.data.result);
    }
  }

  useEffect(() => {
    if (toastErrorMessage) {
      toast({
        title: toastErrorMessage,
        variant: 'top-accent',
        status: 'error',
        duration: 3000,
        isClosable: true
      });
    }
    setToastErrorMessage(undefined);
  }, [toastErrorMessage, toast]);

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
        height="100vh"
        backgroundColor="gray.200"
      >
       
        
        <Flex
          w='full'
          flexDirection="row"
          flex="auto"
          backgroundColor="gray.200"
        >
          
         {getFilterComponent()}
          
          <Stack
            flexDir="column"
            flex="auto"
            mb="2"
            overflowX="auto"
          >
          
          <Box overflowX="auto" flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch">
          {authLoading ?
            <Stack
            flex="auto"
            p="1rem"
            backgroundColor="whiteAlpha.900"
            boxShadow="md"
            h="full"
            w="full"
            >
            <Center>
            <Spinner
                thickness='4px'
                speed='0.65s'
                emptyColor='gray.200'
                color='blue.500'
                size='xl'
            />
            </Center>
            </Stack>
          :
            <Stack
              flex="auto"
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
              h="full"
              w="full"
              justifyContent="left"
              overflowX="auto"
            >
            {hasTrades ? (
            <HStack h="full" w="full" align='top'>
            <VStack w='50%' h='100%'>
            <Heading class="statsheader">
              <Center>
                Statistics
              </Center>
            </Heading>
            
            <Box overflowX="auto" w="100%" h='100%' borderWidth="1px" rounded="lg" >
              <Grid templateColumns='repeat(1, 1fr)' w='100%' h='12%' >
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Total PNL</StatLabel>
                    <StatNumber color={colorChange(trades.stats.total_pnl)}>{pnlValue(formatter.format(trades.stats.total_pnl))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
              <Grid templateColumns='repeat(2, 7fr)' w='100%' h='70%'>
              <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Trades</StatLabel>
                    <StatNumber>{trades.stats.num_trades + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%'  >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Win %</StatLabel>
                    <StatNumber>{percent.format(trades.stats.win_percent/100)}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Wins</StatLabel>
                    <StatNumber>{trades.stats.num_wins + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Losses</StatLabel>
                    <StatNumber>{trades.stats.num_losses + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Day Trades</StatLabel>
                    <StatNumber>{trades.stats.num_day + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Swing Trades</StatLabel>
                    <StatNumber>{trades.stats.num_swing + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Options Trades</StatLabel>
                    <StatNumber>{trades.stats.num_options + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Shares Trades</StatLabel>
                    <StatNumber>{trades.stats.num_shares + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%'  >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Largest Win</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(trades.stats.largest_win))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Largest Loss</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(trades.stats.largest_loss))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Win</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(trades.stats.avg_win))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Loss</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(trades.stats.avg_loss))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
            </Box>
            </VStack>
            <VStack h="full" w="full" rounded="lg">
              <Box overflowX="auto" h="full" w="full" overflow="auto" rounded="lg">
                    <Chart
                      chartType="PieChart"
                      data={
                        [["Trade Type", "Count"], 
                        ["Day Loss", trades.stats.num_day_loss], 
                        ["Swing Loss", trades.stats.num_swing_loss],
                        ["Day Win", trades.stats.num_day_win],
                        ["Swing Win", trades.stats.num_swing_win]
                      ]}
                      options={pieOptionsA}
                    />
              </Box>
              <Box overflowX="auto" h="full" w="full" overflow="auto" rounded="lg">
                    <Chart
                      chartType="PieChart"
                      data={
                        [["Security Type", "Count"], 
                        ["Options Loss", trades.stats.num_options_loss], 
                        ["Shares Loss", trades.stats.num_shares_loss],
                        ["Options Win", trades.stats.num_options_win],
                        ["Shares Win", trades.stats.num_shares_win]
                      ]}
                      options={pieOptionsB}
                    />
              </Box>
            </VStack>
            </HStack>
            ) : (
              <Text>
                No Trade Data To Display
              </Text>
            )}
            </Stack>
          }
          </Box>
          </Stack>
        </Flex>
      </Flex>
  )
}

