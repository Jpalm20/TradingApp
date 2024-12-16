import React, { useEffect, useState, Component } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades, getTradesFiltered, getTradesStats, getTradesStatsFiltered, getPreferences, getAccountValues, setAccountValue, getTradesPage } from '../store/auth'
import { searchTicker, update, reset, updateTrades } from '../store/trade'
import { Link as RouterLink, useNavigate, useHistory, useLocation} from "react-router-dom";
import { Chart } from "react-google-charts";
import { BsFilter } from "react-icons/bs";
import { BiPencil } from "react-icons/bi";
import { IoFilter } from "react-icons/io5";
import moment from 'moment'; 
import 'moment-timezone';
import '../styles/filter.css';
import '../styles/home.css';
import Lottie from "lottie-react";
import animationData from "../lotties/no-data-animation.json";
import { VscTriangleLeft, VscTriangleRight } from "react-icons/vsc";
import { TriangleDownIcon, TriangleUpIcon } from '@chakra-ui/icons';
import getSymbolFromCurrency from 'currency-symbol-map';
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
  Divider,
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

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

export default function Home({ user }) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  const cancelRef = React.useRef();
  const [toastMessage, setToastMessage] = useState(undefined);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const query = useQuery();
  const { trade } = useSelector((state) => state.trade);
  const tradeSuccess = useSelector((state) => state.trade.success);
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
  const hasTrades = ((trades && trades.trades && Object.keys(trades.trades).length >= 0) ? (true):(false));


  const [toggleFilter, setToggleFilter] = useState(false);

  const [filters, setFilters] = useState(false);

  const user_id = user.user_id;

  const [featureFlag, setFeatureFlag] = useState(false);
  const [optInAlertDialog, setOptInAlertDialog] = useState(false);
  const [accountvalue, setAccountvalue] = useState("0");

  // Function to format a value with the currency symbol
  const format = (val, currencyCode) => {
    const currencySymbol = getSymbolFromCurrency(currencyCode);
    return currencySymbol + val;
  };

  // Function to parse a value and remove the currency symbol
  const parse = (val, currencyCode) => {
    const currencySymbol = getSymbolFromCurrency(currencyCode);
    const regex = new RegExp(`^\\${currencySymbol}`);
    return val.replace(regex, '');
  };

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }

  const handleFilterChange = (newFilter) => {
    query.set('filter', newFilter);
    navigate(`?${query.toString()}`);
  };

  function filtersToQueryString(filters) {
    const params = new URLSearchParams();
    for (const key in filters) {
      if (filters[key] !== '') {
        params.append(key, filters[key]);
      }
    }
    return params.toString();
  }

  useEffect(() => {
    const savedHomeFilters = window.localStorage.getItem('HomeFilters');
    if (savedHomeFilters) {
      const HomeFilters = JSON.parse(savedHomeFilters);
      setFilterTradeType(HomeFilters.trade_type || "");
      setFilterSecurityType(HomeFilters.security_type || "");
      setFilterTickerName(HomeFilters.ticker_name || "");
      setSelectedTickerValue(HomeFilters.ticker_name || "");
      setFilterSwitchDate(HomeFilters.date_range || "");
      setFilterFromDate(HomeFilters.from_date || "");
      setFilterToDate(HomeFilters.to_date || "");
      setFilters(HomeFilters);
    }
  }, []); // Empty dependency array means this runs once on mount

  

  const today = returnInTZ(new Date().toISOString());
  const [todayAccountValue, setTodayAccountValue] = useState(0);
  const [filter_av_time, setFilterAvDate] = useState("");
  const [avtimeloading, setAvTimeLoading] = useState(false);

  useEffect(() => {
    evaluateAvTime();
  }, [filter_av_time]); 

  const evaluateAvTime = async () => {
    if(filter_av_time !== ''){
      setAvTimeLoading(true);
      const filters = {};
      filters.date = today
      filters.time_frame = filter_av_time;
      await dispatch(getAccountValues({ filters }));
      setAvTimeLoading(false);
    }
  }
  
  const setDateFormat = () => {
    let dateFormat = {
      timeZone: "UTC",
      month: "2-digit",
      day: "2-digit",
    };
    if (filter_av_time === "Month") {
      // Format date differently for Month
      dateFormat = {
        timeZone: "UTC",
        month: "short",
        year: "numeric",
      };
    } else if (filter_av_time === "Year") {
      // Format date differently for Year
      dateFormat = {
        timeZone: "UTC",
        year: "numeric",
      };
    } else {
      // Default format for Day
      dateFormat = {
        timeZone: "UTC",
        month: "2-digit",
        day: "2-digit",
      };
    }
    return dateFormat
  }

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
    const date = today;
    await dispatch(
      setAccountValue({
        accountvalue,
        date
      })
    );
    setFilterAvDate("");
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

  useEffect(() => {
    evaluateTradeSuccess();
  }, [tradeSuccess]); 

  const evaluateSuccess = async () => {
    if(success === true && info && info.result && info.result === "Account Value Set Successfully"){
      setToastMessage(info.result);
      setOptInAlertDialog(false);
      onClose();
      const filters = {};
      filters.date = today
      await dispatch(getPreferences());
      await dispatch(getAccountValues({ filters }));
    }
  }

  const evaluateTradeSuccess = async () => {
    if(tradeSuccess === true && trade && trade.result && trade.result.includes("Trades Updated Successfully")){
      setToastMessage(trade.result);
      let filters = {};
      if(filter_trade_type !== ''){
        filters.trade_type = filter_trade_type;
      }
      if(filter_security_type !== ''){
        filters.security_type = filter_security_type;
      }
      if(filter_ticker_name !== ''){
        filters.ticker_name = filter_ticker_name;
      }
      if(filter_switch_time !== '' && (filter_from_date === '' && filter_to_date === '')){
        filters.date_range = filter_switch_time;
      }
      if(filter_switch_time === '' && (filter_from_date !== '' || filter_to_date !== '')){
        if (filter_from_date !== '' && filter_to_date !== ''){
          filters.from_date = filter_from_date;
          filters.to_date = filter_to_date;
        }else if (filter_from_date !== '' && filter_to_date === ''){
          filters.from_date = filter_from_date;
          filters.to_date = today;
        }
        else if (filter_from_date === '' && filter_to_date !== ''){
          filters.from_date = "1900-01-01";
          filters.to_date = filter_to_date;
        }
      }
      await dispatch(
        getTradesStatsFiltered({
          filters
        })
      );
      handleFilterChange(filtersToQueryString(filters));
      window.localStorage.setItem('HomeFilters', JSON.stringify(filters));
      filters.page = 1;
      filters.numrows = num_results;
      filters.trade_date = 'NULL';
      await dispatch(getTradesPage({ filters }));
      dispatch(
        reset()      
      );
      filters = {};
      filters.date = today
      await dispatch(getAccountValues({ filters }));
      clearFormStates();
      setSelectedRow([]);
      setTradeID(null);
    }
  }

  useEffect(() => {
    if (toastMessage) {
      toast({
        title: toastMessage,
        variant: 'solid',
        status: 'success',
        duration: 10000,
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
  const [filter_from_date, setFilterFromDate] = useState("");
  const [filter_to_date, setFilterToDate] = useState("");
  const [isFromToDisabled, setIsFromToDisabled] = useState(false);
  const [isDateRangeDisabled, setIsDateRangeDisabled] = useState(false);

  // Your logic to enable or disable the input
  useEffect(() => {
    if (filter_switch_time !== '' && (filter_from_date === '' && filter_to_date === '')) {
      setIsFromToDisabled(true);
      setIsDateRangeDisabled(false);
    } else if ((filter_switch_time === '' && (filter_from_date !== '' || filter_to_date !== ''))){
      setIsFromToDisabled(false);
      setIsDateRangeDisabled(true);
    } else if ((filter_switch_time === '' && filter_from_date === '' && filter_to_date === '')){
      setIsFromToDisabled(false);
      setIsDateRangeDisabled(false);
    }
  }, [filter_switch_time,filter_from_date,filter_to_date]);


  const authLoading = useSelector((state) => state.auth.loading);
  const tradeLoading = useSelector((state) => state.trade.loading);


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

  const keysToSkip = ['page', 'numrows', 'trade_date'];
  
  const appliedFilters = Object.entries(filters).filter(([key]) => !keysToSkip.includes(key)).map(([key, value]) => (
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


  const formatter = (currencyCode) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currencyCode,
    });
  };

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
      fontSize: 16,
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
      minValue: 0,
      textStyle: {
        color: '#636363',
        bold: true,
      },
      format: 'decimal',
      //currency: hasPreferences ? preferences.preferred_currency : 'USD',
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
      fontSize: 16,
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
      minValue: 0,
      textStyle: {
        color: '#dfdfdf', 
        bold: true,
      },
      format: 'decimal',
      //currency: hasPreferences ? preferences.preferred_currency : 'INR',
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
                  <Select placeholder='Select Time Frame' value={filter_switch_time} onChange={(e) => setFilterSwitchDate(e.target.value)} disabled={isDateRangeDisabled}>
                    <option>Year</option>
                    <option>Month</option>
                    <option>Week</option>
                    <option>Day</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    From Date
                  </FormHelperText>
                  <Input
                    value={filter_from_date}
                    type="date"
                    max={maxDate}
                    min="1900-01-01"
                    onChange={(e) => setFilterFromDate(e.target.value)}
                    disabled={isFromToDisabled}
                />
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    To Date
                  </FormHelperText>
                  <Input
                    value={filter_to_date}
                    type="date"
                    max={maxDate}
                    min={filter_from_date !== '' ? filter_from_date : "1900-01-01"}
                    onChange={(e) => setFilterToDate(e.target.value)}
                    disabled={isFromToDisabled}
                />
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
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    From Date
                  </FormHelperText>
                  <Input
                    value={filter_from_date}
                    type="date"
                    max={maxDate}
                    min="1900-01-01"
                    onChange={(e) => setFilterFromDate(e.target.value)}
                    disabled={isFromToDisabled}
                />
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    To Date
                  </FormHelperText>
                  <Input
                    value={filter_to_date}
                    type="date"
                    max={maxDate}
                    min={filter_from_date !== '' ? filter_from_date : "1900-01-01"}
                    onChange={(e) => setFilterToDate(e.target.value)}
                    disabled={isFromToDisabled}
                />
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

  const [page, setPage] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [numRows, setNumRows] = useState(0);
  const [num_results, setNumResults] = useState(5);
  const pageStartOffset = (page !== 0) ? ((page*numRows)-(numRows-1)) : 0;
  const pageEndOffset = totalCount < (page*numRows) ? totalCount : (page*numRows);
  const [backPageEnable, setBackPageEnable] = useState(false);
  const [nextPageEnable, setNextPageEnable] = useState(false);
  const [selectedRow, setSelectedRow] = useState([]);
  const [ids, setSelectedTradeIds] = useState([]);
  const [opentradesLoading, setOpenTradesLoading] = useState(false);
  const [closeTradePopup, setCloseTradePopup] = useState(false);
  const [trade_date, setTradeDate] = useState("");

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

  const rrformat = (val1,val2) => val1 + ":" + val2;
  const [risk, setRisk] = useState("1");
  const [reward, setReward] = useState("1");

  useEffect(() => {
    if(risk > 0 && reward > 0 && rr !== rrformat(risk, reward)){
      setRR(rrformat(risk,reward));
    }
  }, [risk, reward]); 

  function clearFormStates() {
    setTradeType("");
    setSecurityType("");
    setTickerName("");
    setSelectedValue("");
    setSearchValue("");
    setTradeDate("");
    setExpiry("");
    setStrike("");
    setBuyValue("");
    setUnits("");
    setRR("");
    setPNL("");
    setPercentWL("");
    setComments("");
    setRisk( "1");
    setReward( "1");
  }


  useEffect(() => {
    if (hasTrades) {
      setPage(parseInt(trades.page));
      setTotalCount(parseInt(trades.count));
      setNumRows(parseInt(trades.numrows));
    }
  }, [trades]); 

  const evaluatePage = () => {
    if(totalCount > 0){
      const pageCount = Math.ceil(totalCount/numRows);
      if(page === pageCount){
        setNextPageEnable(false);
      }else if (page < pageCount){
        setNextPageEnable(true);
      }
    }else{
      setNextPageEnable(false);
    }
    if(page === 1 || page === 0){
      setBackPageEnable(false);
    }else{
      setBackPageEnable(true);
    }
  }

  useEffect(() => {
    evaluatePage();
  }, [page,totalCount,num_results,numRows]);

  const handleNextPage = async (e) => {
    if(nextPageEnable){
      setOpenTradesLoading(true);
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
      if(filter_switch_time !== '' && (filter_from_date === '' && filter_to_date === '')){
        filters.date_range = filter_switch_time;
      }
      if(filter_switch_time === '' && (filter_from_date !== '' || filter_to_date !== '')){
        if (filter_from_date !== '' && filter_to_date !== ''){
          filters.from_date = filter_from_date;
          filters.to_date = filter_to_date;
        }else if (filter_from_date !== '' && filter_to_date === ''){
          filters.from_date = filter_from_date;
          filters.to_date = today;
        }
        else if (filter_from_date === '' && filter_to_date !== ''){
          filters.from_date = "1900-01-01";
          filters.to_date = filter_to_date;
        }
      }
      filters.page = page+1;
      filters.numrows = num_results;
      filters.trade_date = 'NULL';
      await dispatch(getTradesPage({ filters }));  
      setSelectedRow([]);
      setOpenTradesLoading(false);
    }
  }

  const handleBackPage = async (e) => {
    if(backPageEnable){
      setOpenTradesLoading(true);
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
      if(filter_switch_time !== '' && (filter_from_date === '' && filter_to_date === '')){
        filters.date_range = filter_switch_time;
      }
      if(filter_switch_time === '' && (filter_from_date !== '' || filter_to_date !== '')){
        if (filter_from_date !== '' && filter_to_date !== ''){
          filters.from_date = filter_from_date;
          filters.to_date = filter_to_date;
        }else if (filter_from_date !== '' && filter_to_date === ''){
          filters.from_date = filter_from_date;
          filters.to_date = today;
        }
        else if (filter_from_date === '' && filter_to_date !== ''){
          filters.from_date = "1900-01-01";
          filters.to_date = filter_to_date;
        }
      }
      filters.page = page-1;
      filters.numrows = num_results;
      filters.trade_date = 'NULL';
      await dispatch(getTradesPage({ filters }));  
      setSelectedRow([]);
      setOpenTradesLoading(false);
    }
  }

  const handleChangeNumResults = async (e) => {
    const new_num_results = e.target.value;
    setNumResults(new_num_results);
    setOpenTradesLoading(true);
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
    if(filter_switch_time !== '' && (filter_from_date === '' && filter_to_date === '')){
      filters.date_range = filter_switch_time;
    }
    if(filter_switch_time === '' && (filter_from_date !== '' || filter_to_date !== '')){
      if (filter_from_date !== '' && filter_to_date !== ''){
        filters.from_date = filter_from_date;
        filters.to_date = filter_to_date;
      }else if (filter_from_date !== '' && filter_to_date === ''){
        filters.from_date = filter_from_date;
        filters.to_date = today;
      }
      else if (filter_from_date === '' && filter_to_date !== ''){
        filters.from_date = "1900-01-01";
        filters.to_date = filter_to_date;
      }
    }
    filters.page = 1;
    filters.numrows = new_num_results;
    filters.trade_date = 'NULL';
    await dispatch(getTradesPage({ filters }));  
    setSelectedRow([]);
    setOpenTradesLoading(false);
  }

  const handleSelectAll = (e) => {
    if (hasTrades && trades.trades.length === 1) {
      setSelectedRow([]);
      setTradeID(trades.trades[0].trade_id);
      setSelectedRow([...selectedRow, 0]);
    }else if (hasTrades && trades.trades.length > 1){
      setSelectedRow([]);
      setTradeID(null);
      setSelectedRow(Array.from({ length: trades.trades.length }, (_, index) => index));
    }
  }

  const handleClearSelected = (e) => {
    setSelectedRow([]);
    setTradeID(null);
  }

  const handleGotoClose = (e) => {
    setSelectedTradeIds(selectedRow.map(index => trades.trades[index].trade_id));
    setCloseTradePopup(true);
  };

  const handleConfirmClose = async (e) => {
    e.preventDefault();
    setSelectedRow([]);
    setOpenTradesLoading(true);
    setCloseTradePopup(false);
    let update_info = {
      trade_type,
      security_type,
      ticker_name,
      trade_date,
      expiry,
      strike,
      buy_value,
      units,
      rr,
      pnl,
      percent_wl,
      comments
    }
    await dispatch(
      updateTrades({
        ids,
        update_info
      })
    );
    clearFormStates();
    setSelectedTradeIds([]);
    setOpenTradesLoading(false);
  };

  const handleCancelClose = (e) => {
    setSelectedRow([]);
    setCloseTradePopup(false);
    setSelectedTradeIds([]);
    clearFormStates();
  };

  useEffect(() => {
    calculatePercent();
  }, [pnl, buy_value, units]); 

  const calculatePercent = () => {
    const pnlFloat=parseFloat(pnl);
    const buyValueFloat=parseFloat(buy_value);
    const unitsFloat=parseFloat(units);
    if (!isNaN(pnlFloat) && !isNaN(buyValueFloat) && buyValueFloat !== 0 && !isNaN(unitsFloat) && unitsFloat !== 0) {
      setPercentWL(((pnlFloat/(buyValueFloat*unitsFloat)*100).toFixed(2)));
    }else{
      setPercentWL("");
    }
  }

  //sorting logic
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  const sortedTrades = React.useMemo(() => {
    if(hasTrades) {
      let sortableItems = [...trades.trades];
      if (sortConfig.key !== null) {
        sortableItems.sort((a, b) => {
          const aValue = a[sortConfig.key];
          const bValue = b[sortConfig.key];
  
          // Handle null values
          if (aValue === null) return sortConfig.direction === 'asc' ? -1 : 1;
          if (bValue === null) return sortConfig.direction === 'asc' ? 1 : -1;
  
          if (aValue < bValue) {
            return sortConfig.direction === 'asc' ? -1 : 1;
          }
          if (aValue > bValue) {
            return sortConfig.direction === 'asc' ? 1 : -1;
          }
          return 0;
        });
      }
      return sortableItems;
    }
  }, [trades, sortConfig]);

  const requestSort = key => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (key) => {
    if (sortConfig.key === key) {
      return sortConfig.direction === 'asc' ? <TriangleUpIcon /> : <TriangleDownIcon />;
    }
    return <IoFilter />;
  };

  const getOpenTrades = () => {
    let content = [];
    content.push(
      <>
      <Heading class={colorMode === 'light' ? 'statsheadersmall' : 'statsheaderdarksmall'}>
        <Center>
          Open Trades
        </Center>
      </Heading>
      {opentradesLoading ?
        <Stack
        flex="auto"
        p="1rem"
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
      <>
      <Stack
        flex="auto"
        w="full"
      >
      <HStack justifyContent='space-between'>
      <HStack justifyContent='space-between' flexWrap='wrap' overflowX="scroll">
      <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="xs" marginLeft={1} marginBottom={1} width='75px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleSelectAll(e.target.value)}>
        Select All
      </Button>
      <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="xs" marginLeft={1} marginBottom={1} width='50px' backgroundColor='gray.300'  color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleClearSelected(e.target.value)}>
        Clear
      </Button>
      <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="xs" marginLeft={1} marginBottom={1} width='50px' colorScheme='blue' isDisabled={selectedRow.length <= 0} onClick={e => handleGotoClose(e)}>
        Close
      </Button>
      </HStack>
      <AlertDialog
        motionPreset='slideInBottom'
        isOpen={closeTradePopup}
        leastDestructiveRef={cancelRef}
        onClose={e => handleCancelClose(e)}
        isCentered={true}
        size='sm'
        closeOnOverlayClick={true}
      >
        <AlertDialogOverlay>
        <AlertDialogContent>
          <AlertDialogHeader fontSize='lg' fontWeight='bold'>
            Close Trade
          </AlertDialogHeader>

          <AlertDialogBody>
            <FormControl>
              <FormHelperText mb={2} ml={1}>
                Closure Date
              </FormHelperText>
              <Input
                  value={trade_date}
                  type="date"
                  max={maxDate}
                  min="1900-01-01"
                  onChange={(e) => setTradeDate(e.target.value)}
              />
            </FormControl>
            <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Average Cost *
                  </FormHelperText>
                  <Input
                    value={buy_value}
                    type="name"
                    onChange={(e) => setBuyValue(e.target.value)}
                  />
              </FormControl>
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    # of Units *
                  </FormHelperText>
                  <Input
                    value={units}
                    type="name"
                    onChange={(e) => setUnits(e.target.value)}
                  />
              </FormControl>
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    PNL *
                  </FormHelperText>
                  <Input
                    value={pnl}
                    type="name"
                    onChange={(e) => setPNL(e.target.value)}
                  />
              </FormControl>
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    % Win or Loss *
                  </FormHelperText>
                  <Input
                    value={percent_wl}
                    type="name"
                    readOnly
                    placeholder={"0.00"}
                    value={percent_wl}
                  />
              </FormControl>
          </AlertDialogBody>
          <AlertDialogFooter paddingTop={10}>
            <Button ref={cancelRef} minWidth='50px' onClick={e => handleCancelClose(e)}>
              Cancel
            </Button>
            <Button colorScheme='blue' minWidth='50px' isDisabled={!trade_date} onClick={e => handleConfirmClose(e)} ml={3}>
              Submit
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
      </HStack>
      </Stack>
      {hasTrades ?
      <>
      <TableContainer overflowY="auto" overflowX="auto" rounded="lg" h="80%" maxHeight="400px">
        <Table size='sm' variant='simple' colorScheme='gray' borderWidth="1px" borderColor={colorMode === 'light' ? "gray.100" : "gray.800"}>
          <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"} zIndex={2}>
            <Tr>
              <Th resize='horizontal' overflow='auto'>
                <HStack>
                  <span>
                    Trade<br></br>Type
                  </span>
                  <IconButton
                    aria-label="Sort by Trade Type"
                    icon={getSortIcon('trade_type')}
                    onClick={() => requestSort('trade_type')}
                    size="xs"
                    variant="ghost"
                  />
                </HStack>
              </Th>
              <Th resize='horizontal' overflow='auto'>
                <HStack>
                  <span>
                    Security<br></br>Type
                  </span>
                  <IconButton
                    aria-label="Sort by Security Type"
                    icon={getSortIcon('security_type')}
                    onClick={() => requestSort('security_type')}
                    size="xs"
                    variant="ghost"
                  />
                </HStack>
              </Th>
              <Th resize='horizontal' overflow='auto'>
              <HStack>
                <span>
                  Ticker
                </span>
                <IconButton
                  aria-label="Sort by Ticker"
                  icon={getSortIcon('ticker_name')}
                  onClick={() => requestSort('ticker_name')}
                  size="xs"
                  variant="ghost"
                />
              </HStack>
              </Th>
              <Th resize='horizontal' overflow='auto'>
              <HStack>
                <span>
                  # of<br></br>Units
                </span>
                <IconButton
                  aria-label="Sort by # of Units"
                  icon={getSortIcon('units')}
                  onClick={() => requestSort('units')}
                  size="xs"
                  variant="ghost"
                />
              </HStack>
              </Th>
              <Th resize='horizontal' overflow='auto'>
              <HStack>
                <span>
                  Avg<br></br>Price
                </span>
                <IconButton
                  aria-label="Sort by Avg Price"
                  icon={getSortIcon('buy_value')}
                  onClick={() => requestSort('buy_value')}
                  size="xs"
                  variant="ghost"
                />
              </HStack>
              </Th>
            </Tr>
          </Thead>
              <Tbody zIndex={1}>
                {sortedTrades.map((trade, index) => (
                  <Tr
                  onClick={async () => {
                    if (selectedRow.includes(index)) {
                      const filteredSelectedRow = selectedRow.filter((row) => row !== index);
                      await setSelectedRow(filteredSelectedRow);
                      if (selectedRow.length === 2){
                        const indexofIndex = selectedRow.indexOf(index);
                        if(indexofIndex === 0){
                          setTradeID(trades.trades[selectedRow[1]].trade_id);
                        } else{
                          setTradeID(trades.trades[selectedRow[0]].trade_id);
                        }
                      } else if (selectedRow.length === 1) {
                        setTradeID(null);
                      }
                    } else if (!selectedRow.includes(index) && selectedRow.length === 0) {
                      setSelectedRow([...selectedRow, index]); 
                      setTradeID(trade.trade_id);
                    } else if (!selectedRow.includes(index) && selectedRow.length >= 1) {
                      setSelectedRow([...selectedRow, index]); 
                      setTradeID(null);
                    } 
                  }}
                  bgColor={colorMode === 'light' ? selectedRow.includes(index) ? 'lightgrey' : 'white' : selectedRow.includes(index) ? 'gray.900' : "gray.700"}
                  >
                    <Td>{trade.trade_type}</Td>
                    <Td>{trade.security_type}</Td>
                    <Td>{trade.ticker_name}</Td>
                    <Td isNumeric>{trade.units}</Td>
                    <Td isNumeric>{trade.buy_value}</Td>
                  </Tr>
                ))}
              </Tbody>
        </Table>
      </TableContainer>
      <Stack
        flex="auto"
        w="full"
      >
      <HStack justifyContent='end' paddingEnd='1' paddingTop='1' flexWrap='wrap' overflowX="scroll">
        <HStack flexWrap='wrap'>
          <Text class='numresults'>
            No. of Rows:
          </Text>
          <Select maxW={65} minW={65} variant='filled' size="xs" defaultValue='5' value={num_results} onChange={(e) => handleChangeNumResults(e)}>
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
          </Select>
        </HStack>
        <HStack>
          <VscTriangleLeft isDisabled={!backPageEnable} class='pagearrowssmall' onClick={e => handleBackPage(e)}>

          </VscTriangleLeft>
          <VscTriangleRight isDisabled={!nextPageEnable} class='pagearrowssmall' onClick={e => handleNextPage(e)}>

          </VscTriangleRight>
          <Text class='pagenumbers'>
            {pageStartOffset}-{pageEndOffset} of {totalCount}
          </Text>
        </HStack>
      </HStack>
      </Stack>
      </>
      :
      <>
      <TableContainer overflowY="auto" overflowX="auto" rounded="lg" h="80%" maxHeight="400px">
        <Table size='sm' variant='simple' colorScheme='gray' borderWidth="1px" borderColor={colorMode === 'light' ? "gray.100" : "gray.800"}>
          <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"} zIndex={2}>
            <Tr>
              <Th resize='horizontal' overflow='auto'>Trade Type</Th>
              <Th resize='horizontal' overflow='auto'>Security Type</Th>
              <Th resize='horizontal' overflow='auto'>Ticker</Th>
              <Th resize='horizontal' overflow='auto'># of Units</Th>
              <Th resize='horizontal' overflow='auto'>Avg Price</Th>
            </Tr>
          </Thead>
        </Table>
      </TableContainer>
      <HStack justifyContent='end' paddingEnd='1' paddingTop='1' flexWrap='wrap' overflowX="scroll">
        <HStack flexWrap='wrap'>
          <Text class='numresults'>
            No. of Rows:
          </Text>
          <Select maxW={65} minW={65} variant='filled' size="xs" defaultValue='5' value={num_results} onChange={(e) => handleChangeNumResults(e)}>
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
          </Select>
        </HStack>
        <HStack>
          <VscTriangleLeft isDisabled={!backPageEnable} class='pagearrowssmall' onClick={e => handleBackPage(e)}>

          </VscTriangleLeft>
          <VscTriangleRight isDisabled={!nextPageEnable} class='pagearrowssmall' onClick={e => handleNextPage(e)}>

          </VscTriangleRight>
          <Text class='pagenumbers'>
            {pageStartOffset}-{pageEndOffset} of {totalCount}
          </Text>
        </HStack>
      </HStack>
      </>
      }
      </>
      }
      </>
    );
    return content;
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
    if(filter_switch_time !== '' && (filter_from_date === '' && filter_to_date === '')){
      filters.date_range = filter_switch_time;
    }
    if(filter_switch_time === '' && (filter_from_date !== '' || filter_to_date !== '')){
      if (filter_from_date !== '' && filter_to_date !== ''){
        filters.from_date = filter_from_date;
        filters.to_date = filter_to_date;
      }else if (filter_from_date !== '' && filter_to_date === ''){
        filters.from_date = filter_from_date;
        filters.to_date = today;
      }
      else if (filter_from_date === '' && filter_to_date !== ''){
        filters.from_date = "1900-01-01";
        filters.to_date = filter_to_date;
      }
    }
    await dispatch(
      getTradesStatsFiltered({
        filters
      })
    );
    handleFilterChange(filtersToQueryString(filters));
    window.localStorage.setItem('HomeFilters', JSON.stringify(filters));
    filters.page = 1;
    filters.numrows = 5;
    filters.trade_date = 'NULL';
    await dispatch(getTradesPage({ filters }));
    setSelectedRow([]);
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
    setFilterFromDate('');
    setFilterToDate('');
    setSearchTickerValue('');
    setSelectedTickerValue('');
    await dispatch(getTradesStats());
    handleFilterChange(filtersToQueryString({}));
    window.localStorage.removeItem('HomeFilters');
    const filters = {};
    filters.page = 1;
    filters.numrows = 5;
    filters.trade_date = 'NULL';
    await dispatch(getTradesPage({ filters }));
    setFilters({});
    setSelectedRow([]);
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
        duration: 10000,
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
          {authLoading && !optInAlertDialog && !avtimeloading && !opentradesLoading ?
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
            {hasStats && hasPreferences && hasAVs && hasTrades ? (
            <HStack h="full" w="full" align='top'>
            <VStack w='40%' h='100%'>
            <Heading class={colorMode === 'light' ? 'statsheader' : 'statsheaderdark'}>
              <Center>
                Statistics
              </Center>
            </Heading>
            
            <Box overflowX="auto" w="100%" h='100%' borderWidth="1px" rounded="lg" maxHeight="400px">
              <Grid templateColumns='repeat(1, 1fr)' w='100%' h='12%' minHeight='100px' minWidth='250px'>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%'>
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Account Value</StatLabel>
                    <div>
                    {featureFlag ? (
                    <StatNumber style={{ display: 'flex', alignItems: 'center' }}>
                      {format(todayAccountValue,preferences.preferred_currency)} 
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
                    <StatHelpText>{today}</StatHelpText>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
              <Grid templateColumns='repeat(2, 10fr)' w='100%' h='70%' minWidth='250px'>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Total PNL</StatLabel>
                    <StatNumber color={colorChange(stats.stats.total_pnl)}>{pnlValue(formatter(preferences.preferred_currency).format(stats.stats.total_pnl))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Avergae PNL Per Trade</StatLabel>
                    <StatNumber color={colorChange(stats.stats.total_pnl)}>{pnlValue(formatter(preferences.preferred_currency).format(stats.stats.avg_pnl))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
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
                    <StatNumber>{pnlValue(formatter(preferences.preferred_currency).format(stats.stats.largest_win))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Largest Loss</StatLabel>
                    <StatNumber>{pnlValue(formatter(preferences.preferred_currency).format(stats.stats.largest_loss))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Win</StatLabel>
                    <StatNumber>{pnlValue(formatter(preferences.preferred_currency).format(stats.stats.avg_win))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Loss</StatLabel>
                    <StatNumber>{pnlValue(formatter(preferences.preferred_currency).format(stats.stats.avg_loss))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Shares Per Trade</StatLabel>
                    <StatNumber>{stats.stats.avg_shares_per_trade}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' p='1' w='100%' h='100%' >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Average Contracts Per Trade</StatLabel>
                    <StatNumber>{stats.stats.avg_options_per_trade}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
            </Box>
            {getOpenTrades()}
            </VStack>
            <VStack h="full" w="full" rounded="lg">
            <HStack h="60%" w="full">
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
                <div className="chart-container">
                  {!avtimeloading ? (
                  <>
                  <Chart
                    chartType="LineChart"
                    width="100%"
                    height="400px"
                    data={
                      [["Date", "Value"], 
                      ...accountValues.accountvalues.map(({ date, accountvalue }) => [new Date(date).toLocaleDateString('en-US', setDateFormat()), accountvalue]),
                    ]}
                    options={colorMode === 'light' ? lineOptions : lineOptionsDark}
                  />
                  <div className="select-bar">
                    <Select variant='flushed' size="sm" defaultValue='Day' value={filter_av_time} onChange={(e) => setFilterAvDate(e.target.value)}>
                      <option value="Day">Day</option>
                      <option value="Week">Week</option>
                      <option value="Month">Month</option>
                      <option value="Year">Year</option>  
                    </Select>
                  </div>
                  </>
                  ) : (
                  <Center>
                    <Spinner
                        thickness='4px'
                        speed='0.65s'
                        emptyColor='gray.200'
                        color='blue.500'
                        size='xl'
                    />
                  </Center>
                  )}
                </div>
              ) : (
                <div style={{ position: 'relative' }} overflow="auto">
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
                            value={format(accountvalue,preferences.preferred_currency)}
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
                            value={format(accountvalue,preferences.preferred_currency)}
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

