import React, { useEffect, useState, Component } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades, getTradesFiltered, getTradesStats, getTradesStatsFiltered, getPreferences, getAccountValues, setAccountValue } from '../store/auth'
import { searchTicker } from '../store/trade'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import { Chart } from "react-google-charts";
import { BsFilter } from "react-icons/bs";
import { BiPencil } from "react-icons/bi";
import '../styles/filter.css';
import '../styles/home.css';
import Lottie from "lottie-react";
import animationData from "../lotties/no-data-animation.json";
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
  IconButton,
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
  useColorMode,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
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
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  const cancelRef = React.useRef();
  const [toastMessage, setToastMessage] = useState(undefined);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trades } = useSelector((state) => state.auth);
  const { stats } = useSelector((state) => state.auth);
  const { preferences } = useSelector((state) => state.auth);
  const { accountValues } = useSelector((state) => state.auth);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const { success } = useSelector((state) => state.auth);
  const hasStats = ((stats && stats.stats && Object.keys(stats.stats).length > 0 && stats.stats.num_trades > 0) ? (true):(false)); //need to look into this for home error
  const hasPreferences = ((preferences && Object.keys(preferences).length > 0) ? (true):(false)); //need to look into this for home error
  const hasAVs = ((accountValues && accountValues.accountvalues && Object.keys(accountValues.accountvalues).length > 0) ? (true):(false)); //need to look into this for home error
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false));

  const [toggleFilter, setToggleFilter] = useState(false);

  const [filters, setFilters] = useState(false);

  const user_id = user.user_id;

  const [featureFlag, setFeatureFlag] = useState(false);
  const [optInAlertDialog, setOptInAlertDialog] = useState(false);
  const [accountvalue, setAccountvalue] = useState("0");

  const format = (val) => `$` + val
  const parse = (val) => val.replace(/^\$/, '')

  const today = new Date().toISOString().split('T')[0];
  const [todayAccountValue, setTodayAccountValue] = useState(0);

  useEffect(() => {
    if(hasAVs && featureFlag){
      setTodayAccountValue(accountValues.accountvalues.find((item) => item.date === today)?.accountvalue);
      setAccountvalue(todayAccountValue);
    }
  }, [accountValues,todayAccountValue]); 


  const handleOptInButton = (e) => {
    e.preventDefault();
    setOptInAlertDialog(true);
  };

  const handleConfirmOptIn = async (e) => {
    e.preventDefault();
    await dispatch(
      setAccountValue({
        accountvalue
      })
    );
    featureFlag ? setAccountvalue(todayAccountValue) : setAccountvalue("0");
  };

  const handleCancelOptIn = (e) => {
    setOptInAlertDialog(false);
    featureFlag ? setAccountvalue(todayAccountValue) : setAccountvalue("0");
    onClose();
  };

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  const evaluateSuccess = async () => {
    if(success === true && info && info.result && info.result === "Account Value Set Successfully"){
      setToastMessage(info.result);
      setOptInAlertDialog(false);
      onClose();
      await dispatch(getPreferences());
      await dispatch(getAccountValues());
    }
  }

  useEffect(() => {
    if (toastMessage) {
      toast({
        title: toastMessage,
        variant: 'solid',
        status: 'success',
        duration: 3000,
        isClosable: true
      });
    }
    setToastMessage(undefined);
  }, [toastMessage, toast]);

  const [trade_id, setTradeID] = useState(null);

  const [filter_trade_type, setFilterTradeType] = useState("");
  const [filter_security_type, setFilterSecurityType] = useState("");
  const [filter_ticker_name, setFilterTickerName] = useState("");
  const [filter_switch_time, setFilterSwitchDate] = useState("");

  const authLoading = useSelector((state) => state.auth.loading);

  const { colorMode, toggleColorMode } = useColorMode();


  const [searchValue, setSearchValue] = useState('');
  const [searchTickerValue, setSearchTickerValue] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchTickerResults, setSearchTickerResults] = useState([]);
  const [selectedValue, setSelectedValue] = useState('');
  const [selectedTickerValue, setSelectedTickerValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);


  useEffect(() => {
    const fetchSearchResults = async () => {
      setIsLoading(true);
      const filter = {};
      if(searchTickerValue !== ''){
        filter.ticker_name = searchTickerValue;
      }
      const response = await dispatch(searchTicker({filter})); 
      const topResults = response.payload.tickers.map(f => [f.ticker_name]);
      setSearchTickerResults(topResults);
      setIsLoading(false);
    };

    if (searchTickerValue) {
      fetchSearchResults();
      setIsDropdownOpen(true);
    } else {
      setSearchTickerResults([]);
      setIsDropdownOpen(false);
    }
  }, [searchTickerValue]);

  const handleInputTickerFilterChange = (event) => {
    setSelectedTickerValue('');
    setSearchTickerValue(event.target.value);
    setFilterTickerName(event.target.value);
  };

  const handleInputTickerFIlterClick = (event) => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleTickerSelection = (selection) => {
    const selectionString = selection[0];
    setSelectedTickerValue(selectionString);
    setFilterTickerName(selectionString);
    setIsDropdownOpen(false);
  };

  const searchTickerResultItems = searchTickerResults.map((result) => (
    <li key={result} onClick={() => handleTickerSelection(result)}> 
      {result}
    </li>
  ));

  const appliedFilters = Object.entries(filters).map(([key, value]) => (
    <Tr key={key}>
      <Td>{key}</Td>
      <Td>{value}</Td>
    </Tr>
  ));


  const appliedFiltersComponent = () => {
    let content = [];
    if(Object.keys(filters).length !== 0){
      content.push(
        <TableContainer>
          <Table variant='simple' size='sm'>
            <TableCaption placement="top">
                Applied Filters
            </TableCaption>
            <Thead>
              <Tr>
                <Th>Filter</Th>
                <Th>Value</Th>
              </Tr>
            </Thead>
            <Tbody>
              {appliedFilters}
            </Tbody>
          </Table>
        </TableContainer>
      );
    }
    return content
  };



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
      textStyle: {
        color: '#636363',
        fontName: 'Open Sans',
      },
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
      textStyle: {
        color: '#636363',
        fontName: 'Open Sans',
      },
    },
  };

  const lineOptions = {
    title: "Account Value",
    legend: 'none',
    curveType: "linear",
    backgroundColor: "#FDFDFD",
    titleTextStyle: {
      color: '#636363',
      fontName: 'Open Sans',
      bold: true,
      fontSize: 18,
    },
    hAxis: {
      textStyle: {
        color: '#636363',
        bold: true,
      },
      gridlines: {
        color: 'none', // Remove vertical axis gridlines
      },
    },
    vAxis: {
      textStyle: {
        color: '#636363',
        bold: true,
      },
      format: 'currency',
      gridlines: {
        color: 'none', // Remove vertical axis gridlines
      },
    },
  };

  const pieOptionsAdark = {
    title: "Day Trade vs Swing Trade",
    chartArea: {
      width: "80%",
      height: "75%"
    },
    height: "100%",
    width: "100%",
    backgroundColor: "#1a202c",
    titleTextStyle: {
      color: '#dfdfdf',
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
      textStyle: {
        color: '#dfdfdf',
        fontName: 'Open Sans',
      },
    },
  };

  const pieOptionsBdark = {
    title: "Options vs Shares",
    chartArea: {
      width: "80%",
      height: "75%"
    },
    height: "100%",
    width: "100%",
    backgroundColor: "#1a202c",
    titleTextStyle: {
      color: '#dfdfdf',
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
      textStyle: {
        color: '#dfdfdf',
        fontName: 'Open Sans',
      },
    },
  };

  const lineOptionsDark = {
    title: "Account Value",
    legend: 'none',
    curveType: "linear",
    backgroundColor: "#1a202c",
    series: {
      0: { // Specify the series index (0 in this example)
        color: '#90CAF9', // Change the color of the line
      },
    },
    titleTextStyle: {
      color: '#dfdfdf',
      fontName: 'Open Sans',
      bold: true,
      fontSize: 18,
    },
    hAxis: {
      textStyle: {
        color: '#dfdfdf',
        bold: true,
      },
      gridlines: {
        color: 'none', // Remove vertical axis gridlines
      },
    },
    vAxis: {
      textStyle: {
        color: '#dfdfdf', 
        bold: true,
      },
      format: 'currency',
      gridlines: {
        color: 'none', // Remove vertical axis gridlines
      },
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
                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
                boxShadow="md"
                align='center'
                minWidth="30vh"
              >
                <Heading class={colorMode === 'light' ? "filterheader" : "filterheaderdark"}>Filters</Heading>
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
                  <div class="ticker-search">
                    <Input type="name" placeholder='Enter Ticker' value={selectedTickerValue ? selectedTickerValue : searchTickerValue} onChange={handleInputTickerFilterChange} onClick={handleInputTickerFIlterClick}/>
                    {isDropdownOpen && (
                      <ul class={colorMode === 'light' ? "search-dropdown" : "search-dropdowndark"}>
                        {isLoading ? (
                          <div>Loading...</div>
                        ) : (
                          searchTickerResultItems
                        )}
                      </ul>
                    )}
                  </div>                
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
                  <Button size="sm" backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} width="full" onClick={handleSubmitFilter} >
                    Submit Filter
                  </Button>
                  <Button size="sm" colorScheme='red' width="full" onClick={handleClearFilter} >
                    Clear Filter
                  </Button>
                {appliedFiltersComponent()}
              </Stack>
            </Box>
          </div>
    );
    content.push(
      <div padd class="small-component">
      <Box flexGrow="1"  backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"} display="flex" borderWidth="1px" h="100%" rounded="lg" overflow="hidden" alignItems="stretch">
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
          <DrawerHeader class={colorMode === 'light' ? "smallfilterheader" : "smallfilterheaderdark"}>Filters</DrawerHeader>

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
                  <div class="ticker-search">
                    <Input type="name" placeholder='Enter Ticker' value={selectedTickerValue ? selectedTickerValue : searchTickerValue} onChange={handleInputTickerFilterChange} onClick={handleInputTickerFIlterClick}/>
                    {isDropdownOpen && (
                      <ul class={colorMode === 'light' ? "search-dropdown" : "search-dropdowndark"}>
                        {isLoading ? (
                          <div>Loading...</div>
                        ) : (
                          searchTickerResultItems
                        )}
                      </ul>
                    )}
                  </div>                
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
                {appliedFiltersComponent()}
          </DrawerBody>

          <DrawerFooter>
            <Button size="sm" backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} width="full" onClick={handleSubmitFilter}>
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
      getTradesStatsFiltered({
        filters
      })
    );
    setFilters(filters);
    //setToggleFilter(!toggleFilter);
  }

  const handleClearFilter = async (e) => {
    e.preventDefault();
    onClose();
    setFilterTradeType('');
    setFilterSecurityType('');
    setFilterTickerName('');
    setFilterSwitchDate('');
    setSearchTickerValue('');
    setSelectedTickerValue('');
    await dispatch(getTradesStats());
    setFilters({});
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
    evaluatePreferences();
  }, [preferences]); 

  const evaluatePreferences = () => {
    if(preferences && preferences.account_value_optin === 1){
      setFeatureFlag(true);
    }else{
      setFeatureFlag(false);
    }
  }

  useEffect(() => {
    if (toastErrorMessage) {
      toast({
        title: toastErrorMessage,
        variant: 'solid',
        status: 'error',
        duration: 3000,
        isClosable: true
      });
    }
    setToastErrorMessage(undefined);
  }, [toastErrorMessage, toast]);

  const handleLogTrade = (e) => {
    navigate("/logTrade");
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
        height="100vh"
        backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
      >
       
        
        <Flex
          w='full'
          flexDirection="row"
          flex="auto"
          backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
        >
          
         {getFilterComponent()}
          
          <Stack
            flexDir="column"
            flex="auto"
            mb="2"
            overflowX="auto"
          >
          
          <Box overflowX="auto" flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch">
          {authLoading && !optInAlertDialog ?
            <Stack
            flex="auto"
            p="1rem"
            backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
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
              backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
              boxShadow="md"
              h="full"
              w="full"
              justifyContent="left"
              overflowX="auto"
            >
            {hasStats && hasPreferences && hasAVs ? (
            <HStack h="full" w="full" align='top'>
            <VStack w='30%' h='100%'>
            <Heading class={colorMode === 'light' ? 'statsheader' : 'statsheaderdark'}>
              <Center>
                Statistics
              </Center>
            </Heading>
            
            <Box overflowX="auto" w="100%" h='100%' borderWidth="1px" rounded="lg" >
              <Grid templateColumns='repeat(2, 1fr)' w='100%' h='12%' minHeight='100px' minWidth='250px'>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Total PNL</StatLabel>
                    <StatNumber color={colorChange(stats.stats.total_pnl)}>{pnlValue(formatter.format(stats.stats.total_pnl))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%'>
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Account Value</StatLabel>
                    <div>
                    {featureFlag ? (
                    <StatNumber style={{ display: 'flex', alignItems: 'center' }}>
                      {format(todayAccountValue)} 
                    <IconButton
                      marginLeft={2}
                      colorScheme='gray'
                      aria-label='update account value'
                      size="xs"
                      icon={<Icon as={BiPencil} />}
                      onClick={e => handleOptInButton(e)}
                    />
                    </StatNumber>
                    ) : (
                    <StatNumber style={{ display: 'flex', alignItems: 'center' }}>
                      N/A
                    </StatNumber>                     
                    )}
                    </div>
                    <StatHelpText>{new Date(today).toLocaleDateString('en-US', { timeZone: 'UTC'})}</StatHelpText>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
              <Grid templateColumns='repeat(2, 7fr)' w='100%' h='70%' minWidth='250px'>
              <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Trades</StatLabel>
                    <StatNumber>{stats.stats.num_trades + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%'  >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Win %</StatLabel>
                    <StatNumber>{percent.format(stats.stats.win_percent/100)}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Wins</StatLabel>
                    <StatNumber>{stats.stats.num_wins + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Losses</StatLabel>
                    <StatNumber>{stats.stats.num_losses + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Day Trades</StatLabel>
                    <StatNumber>{stats.stats.num_day + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Swing Trades</StatLabel>
                    <StatNumber>{stats.stats.num_swing + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Options Trades</StatLabel>
                    <StatNumber>{stats.stats.num_options + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># of Shares Trades</StatLabel>
                    <StatNumber>{stats.stats.num_shares + " Trades"}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%'  >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Largest Win</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(stats.stats.largest_win))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Largest Loss</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(stats.stats.largest_loss))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Win</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(stats.stats.avg_win))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Loss</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(stats.stats.avg_loss))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
            </Box>
            </VStack>
            <VStack h="full" w="full" rounded="lg">
            <HStack h="70%" w="full">
              <Box overflowX="auto" h="full" w="full" overflow="auto" rounded="lg">
                    <Chart
                      chartType="PieChart"
                      data={
                        [["Trade Type", "Count"], 
                        ["Day Loss", stats.stats.num_day_loss], 
                        ["Swing Loss", stats.stats.num_swing_loss],
                        ["Day Win", stats.stats.num_day_win],
                        ["Swing Win", stats.stats.num_swing_win]
                      ]}
                      options={colorMode === 'light' ? pieOptionsA : pieOptionsAdark}
                    />
              </Box>
              <Box overflowX="auto" h="full" w="full" overflow="auto" rounded="lg">
                    <Chart
                      chartType="PieChart"
                      data={
                        [["Security Type", "Count"], 
                        ["Options Loss", stats.stats.num_options_loss], 
                        ["Shares Loss", stats.stats.num_shares_loss],
                        ["Options Win", stats.stats.num_options_win],
                        ["Shares Win", stats.stats.num_shares_win]
                      ]}
                      options={colorMode === 'light' ? pieOptionsB : pieOptionsBdark}
                    />
              </Box>
            </HStack>
            <Box overflowX="auto" h="full" w="full" overflow="auto" rounded="lg">
              {featureFlag ? (
                <Chart
                  chartType="LineChart"
                  width="100%"
                  height="400px"
                  data={
                    [["Date", "Value"], 
                    ...accountValues.accountvalues.map(({ date, accountvalue }) => [new Date(date).toLocaleDateString('en-US', { timeZone: 'UTC', month: '2-digit', day: '2-digit' }), accountvalue]),
                  ]}
                  options={colorMode === 'light' ? lineOptions : lineOptionsDark}
                />
              ) : (
                <div style={{ position: 'relative' }} overflow="auto">
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={
                      [["Date", "Value"], 
                      ...accountValues.accountvalues.map(({ date, accountvalue }) => [new Date(date).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' }), accountvalue]),
                    ]}
                    options={colorMode === 'light' ? lineOptions : lineOptionsDark}
                  />
                  <div 
                    style={
                      colorMode === 'light' ? 
                      {
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        background: 'rgba(255, 255, 255, 0.85)',
                      }
                      : 
                      {
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        background: 'rgba(26, 32, 44, 0.9)',
                      }
                    }
                  />
                  <div
                    style={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      transform: 'translate(-50%, -50%)',
                      textAlign: 'center',
                      padding: '10px 20px',
                    }}
                  >
                  <Text class={colorMode === 'light' ? "avfeatureflagprompt" : "avfeatureflagpromptdark"}>
                    Track Your Progress: Start Tracking Your Account Value
                  </Text>
                  <Button
                    onClick={e => handleOptInButton(e)}
                  >
                    Enter Account Value
                  </Button>
                  </div>
                </div>
              )}  
              {optInAlertDialog}
                  <AlertDialog
                    motionPreset='slideInBottom'
                    isOpen={optInAlertDialog}
                    leastDestructiveRef={cancelRef}
                    onClose={e => handleCancelOptIn(e)}
                    isCentered={true}
                    closeOnOverlayClick={false}
                  >
                  {authLoading && optInAlertDialog ?
                  <AlertDialogOverlay>
                    <AlertDialogContent>
                    <Center>
                      <Spinner
                          thickness='4px'
                          speed='0.65s'
                          emptyColor='gray.200'
                          color='blue.500'
                          size='xl'
                      />
                    </Center>
                    </AlertDialogContent>
                  </AlertDialogOverlay>
                  :
                    <AlertDialogOverlay>
                    <AlertDialogContent>
                      <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                        {hasPreferences && preferences.account_value_optin === 0 ? "Set Account Value" : "Update Account Value"}
                      </AlertDialogHeader>

                      <AlertDialogBody>
                        <FormControl>
                          <FormHelperText mb={2} ml={1}>
                            Current Account Value
                          </FormHelperText>
                          {!featureFlag ? (
                          <NumberInput
                            onChange={(valueString) => setAccountvalue(parse(valueString))}
                            value={format(accountvalue)}
                            min={0}
                          >
                            <NumberInputField />
                            <NumberInputStepper>
                              <NumberIncrementStepper />
                              <NumberDecrementStepper />
                            </NumberInputStepper>
                          </NumberInput>
                          ) : (
                          <NumberInput
                            onChange={(valueString) => setAccountvalue(parse(valueString))}
                            value={format(accountvalue)}
                            min={0}
                          >
                            <NumberInputField />
                            <NumberInputStepper>
                              <NumberIncrementStepper />
                              <NumberDecrementStepper />
                            </NumberInputStepper>
                          </NumberInput>
                          )}
                        </FormControl>
                      </AlertDialogBody>

                      <AlertDialogFooter>
                        <Button ref={cancelRef} onClick={e => handleCancelOptIn(e)}>
                          Cancel
                        </Button>
                        <Button colorScheme='blue' onClick={e => handleConfirmOptIn(e)} ml={3}>
                          Submit
                        </Button>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                    </AlertDialogOverlay>
                  }
                  </AlertDialog>
              </Box>
            </VStack>
            </HStack>
            ) : (
              <Center>
              <VStack marginTop={20}>
              <Lottie animationData={animationData} loop={true} />
              <Text class='no-trade-text'>
                No Trade Data To Display, Please Add Trades  
              </Text>
              <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" width='100px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleLogTrade(e.target.value)}>
                + Add Trade
              </Button>
              </VStack>
              </Center>
            )}
            </Stack>
          }
          </Box>
          </Stack>
        </Flex>
      </Flex>
  )
}

