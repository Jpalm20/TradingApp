import React, { useEffect, useState, Component } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getPnlByYear, getPnlByYearFiltered, getTradesOfDateFiltered } from '../store/auth';
import { searchTicker } from '../store/trade'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import monthsString from "../data/months";
import { BsFilter } from "react-icons/bs";
import '../styles/filter.css';

import {
  Flex,
  Center,
  Text,
  Icon,
  HStack,
  VStack,
  Heading,
  Input,
  Button,
  Spinner,
  Badge,
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
  Stack,
  useColorMode,
  StackDivider,
  useDisclosure,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  Select,
  chakra,
  Toast,
  useToast,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
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
  const btnRef = React.useRef()
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { pnlYTD } = useSelector((state) => state.auth);
  const trades = useSelector((state) => state.auth.tradesOfDay);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const hasPnLInfo = ((pnlYTD && Object.keys(pnlYTD).length > 0 && pnlYTD.months && Object.keys(pnlYTD.months).length > 0) ? (true):(false));
  const hasTradesofDay = ((trades && Object.keys(trades).length > 0 && trades.trades && Object.keys(trades.trades).length > 0) ? (true):(false));
  const hasStats = ((trades && Object.keys(trades).length > 0 && trades.stats && Object.keys(trades.stats).length > 0) ? (true):(false));

  const [toggleFilter, setToggleFilter] = useState(false);

  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();

  const [calDay, setCalDay] = useState(0);
  const [calStartWeek, setCalStartWeek] = useState(0);
  const [calEndWeek, setCalEndWeek] = useState(0);
  const [calMonth, setCalMonth] = useState(month);
  const [calYear, setCalYear] = useState(year);

  const user_id = user.user_id;

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();

  const [filterDrawer, setFilterDrawer] = useState(false);

  const [tradesOfDayPopUp, setTradesOfDayPopUp] = useState(false);
  const [tradesOfWeekPopUp, setTradesOfWeekPopUp] = useState(false);
  const [tradesOfMonthPopUp, setTradesOfMonthPopUp] = useState(false);


  const [filter_trade_type, setFilterTradeType] = useState("");
  const [filter_security_type, setFilterSecurityType] = useState("");
  const [filter_ticker_name, setFilterTickerName] = useState("");

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

  const [filters, setFilters] = useState({});


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

  const handleTradesOfDay = async (e, cal_day) => {
    e.preventDefault();
    setTradesOfDayPopUp(true);
    setCalDay(cal_day);
    const cal_date = new Date(calYear,calMonth,cal_day);
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
    filters.trade_date = cal_date.toISOString().split('T')[0]
    await dispatch(
      getTradesOfDateFiltered({
        filters
      })
    );
  };

  function getWeekDateRange(year, month, week) {
    // Start with the first day of the given month
    const firstDayOfMonth = new Date(year, month, 1);

    // Get the day of the week for the first day of the month
    const firstDayOfWeek = firstDayOfMonth.getDay();

    // Calculate the date of the first day of the given week
    let startDate = new Date(
        year,
        month,
        1 + (week - 1) * 7 - firstDayOfWeek
    );

    // Calculate the date of the last day of the given week
    let endDate = new Date(
        startDate.getFullYear(),
        startDate.getMonth(),
        startDate.getDate() + 6
    );

    // Ensure the startDate is not earlier than the first day of the month
    if (startDate < firstDayOfMonth) {
      startDate = firstDayOfMonth;
    }

    // Get the last day of the given month
    const lastDayOfMonth = new Date(year, month + 1, 0);

    // Ensure the endDate is not later than the last day of the month
    if (endDate > lastDayOfMonth) {
        endDate = lastDayOfMonth;
    }

    return { startDate, endDate };
  }

  const handleTradesOfWeek = async (e, week_index) => {
    e.preventDefault();
    setTradesOfWeekPopUp(true);
    const { startDate, endDate } = getWeekDateRange(calYear,calMonth,week_index);
    setCalStartWeek(startDate);
    setCalEndWeek(endDate);
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
    filters.from_date = startDate.toISOString().split('T')[0]
    filters.to_date = endDate.toISOString().split('T')[0]
    await dispatch(
      getTradesOfDateFiltered({
        filters
      })
    );
  };

  const handleTradesOfMonth = async (e) => {
    e.preventDefault();
    setTradesOfMonthPopUp(true);
    let startDate = new Date(calYear,calMonth, 1);
    let endDate = new Date(calYear,calMonth+1, 0);
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
    filters.from_date = startDate.toISOString().split('T')[0]
    filters.to_date = endDate.toISOString().split('T')[0]
    await dispatch(
      getTradesOfDateFiltered({
        filters
      })
    );
  };

  const handleCancelTradesOfDay = (e) => {
    setTradesOfDayPopUp(false);
    setTradesOfWeekPopUp(false);
    setTradesOfMonthPopUp(false);
    onClose();
  };

  const handleCancelTradesOfWeek = (e) => {
    setTradesOfWeekPopUp(false);
    setTradesOfDayPopUp(false);
    setTradesOfMonthPopUp(false);
    onClose();
  };

  const handleCancelTradesOfMonth = (e) => {
    setTradesOfWeekPopUp(false);
    setTradesOfDayPopUp(false);
    setTradesOfMonthPopUp(false);
    onClose();
  };

  const colorChange = (pnl) => {
    let bgColor;
    if (pnl > 0){
      bgColor = (colorMode === 'light' ? "green.200" : "green.400");
    } else if (pnl < 0) {
      bgColor = (colorMode === 'light' ? "red.200" : "red.400");
    } else {
      bgColor = (colorMode === 'light' ? "gray.100" : "gray.700");
    }
    return bgColor;
  };

  const colorChangeDay = (pnl) => {
    let bgColor;
    if (pnl > 0){
      bgColor = "green.400"
    } else if (pnl < 0) {
      bgColor = "red.400"
    } else {
      bgColor = (colorMode === 'light' ? "black" : "white");
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

  const getDays = (yearr, monthh) => {
    return new Date(yearr, monthh, 0).getDate();
  };

  const getBlanksForFirstDay = () => {
    let content = [];
    let firstDay = new Date(calYear, calMonth, 1).getDay();
    for (let i = 0; i < firstDay; i++) {
      content.push(<GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                </GridItem>);
    }
    return content;
  };

  const getBlanksForEndOfMonth = () => {
    let content = [];
    let totalDays = getDays(calYear, calMonth+1);
    let firstDay = new Date(calYear, calMonth, 1).getDay();
    let spotsLeft = 42-totalDays-firstDay;
    for (let i = 0; i < spotsLeft; i++) {
      content.push(<GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                </GridItem>);
    }
    return content;
  };

  const getMonthlyTotal = () => {
    let monthlyTotal = 0;
    for (let i = 0; i < 31; i++) {
      monthlyTotal += pnlYTD.months[calMonth][calMonth][i]['pnl']
    }
    return monthlyTotal;
  };

  const getGreenDayTotal = () => {
    let greenDayTotal = 0;
    for (let i = 0; i < 31; i++) {
      if(pnlYTD.months[calMonth][calMonth][i]['pnl'] > 0){
        greenDayTotal += 1
      }
    }
    return greenDayTotal;
  };

  const getRedDayTotal = () => {
    let redDayTotal = 0;
    for (let i = 0; i < 31; i++) {
      if(pnlYTD.months[calMonth][calMonth][i]['pnl'] < 0){
        redDayTotal += 1
      }
    }
    return redDayTotal;
  };

  const getGreenDayPercent = () => {
    let greenDays = 0;
    let totalTradeDays = 0;
    let totalDays = getDays(calYear, calMonth);
    for (let i = 0; i < totalDays; i++) {
      if(pnlYTD.months[calMonth][calMonth][i]['pnl'] > 0){
        greenDays += 1
      }
      if(pnlYTD.months[calMonth][calMonth][i]['count'] > 0){
        totalTradeDays += 1
      }
    }
    if(totalTradeDays > 0){
      return (greenDays/totalTradeDays);
    } else {
      return (0);
    }
    
  };

  const getRedDayPercent = () => {
    let redDays = 0;
    let totalTradeDays = 0;
    let totalDays = getDays(calYear, calMonth);
    for (let i = 0; i < totalDays; i++) {
      if(pnlYTD.months[calMonth][calMonth][i]['pnl'] < 0){
        redDays += 1
      }
      if(pnlYTD.months[calMonth][calMonth][i]['count'] > 0){
        totalTradeDays += 1
      }
    }
    if(totalTradeDays > 0){
      return (redDays/totalTradeDays);
    } else {
      return (0);
    }
    
  };

  const getBreakevenDayPercent = () => {
    let evenDays = 0;
    let totalTradeDays = 0;
    let totalDays = getDays(calYear, calMonth);
    for (let i = 0; i < totalDays; i++) {
      if(pnlYTD.months[calMonth][calMonth][i]['pnl'] === 0 && pnlYTD.months[calMonth][calMonth][i]['count'] > 0){
        evenDays += 1
      }
      if(pnlYTD.months[calMonth][calMonth][i]['count'] > 0){
        totalTradeDays += 1
      }
    }
    if(totalTradeDays > 0){
      return (evenDays/totalTradeDays);
    } else {
      return (0);
    }
    
  };

  const getWeeklyTotals = () => {
    let content = [];
    let weekTotals = [0.0,0.0,0.0,0.0,0.0,0.0];
    let weekCounts = [0.0,0.0,0.0,0.0,0.0,0.0];
    let weekCount = 0;
    let dayCount = 0;
    let pnlDayCount = 0;
    let firstDay = new Date(calYear, calMonth, 1).getDay();
    const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();

    const totalDays = firstDay + daysInMonth;
    const numberOfWeeks = Math.ceil(totalDays / 7);

    while (weekCount < numberOfWeeks) {
      if(dayCount !== 0 && dayCount%7 === 0){
        weekCount += 1;
      }
      if (weekCount === 0 && dayCount === 0 && firstDay !== 0) {
        dayCount += firstDay;
      }
      if(pnlYTD.months[calMonth][calMonth][pnlDayCount]?.pnl !== 0.0 && pnlDayCount < daysInMonth){
        weekTotals[weekCount] += pnlYTD.months[calMonth][calMonth][pnlDayCount]?.pnl ?? 0;
      }
      if(pnlYTD.months[calMonth][calMonth][pnlDayCount]?.count !== 0.0 && pnlDayCount < daysInMonth){
        weekCounts[weekCount] += pnlYTD.months[calMonth][calMonth][pnlDayCount]?.count ?? 0;
      }
      dayCount += 1;
      pnlDayCount += 1;
    }
    for (let i = 0; i < numberOfWeeks; i++) {
      content.push(<GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100%' h='100%' _hover={{ bg: "gray.400" }} bg={colorChange(weekTotals[i])} onClick={e => handleTradesOfWeek(e, i+1)}>
                  <Text fontWeight='bold'>-</Text>
                  <Center padding={1}>
                    {weekCounts[i]} Trade(s)
                  </Center>
                  <Center fontWeight='bold' isNumeric>
                    {pnlValue(formatter.format(weekTotals[i]))}
                  </Center>
                </GridItem>);
    }
    for (let i = numberOfWeeks; i < 6; i++) {
      content.push(<GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100%' h='100%' bg={colorChange(0)}></GridItem>);
    }
    return content;
  };

  /*
  const getPnlDays = () => {
    let content = pnlYTD.months[calMonth][calMonth].map((pnl, index) => ( 
      <GridItem key={index} boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' _hover={{ bg: "gray.400" }} bg={colorChange(pnl['pnl'])} onClick={e => handleTradesOfDay(e, index+1)}>
          <Text fontWeight='bold'>{index + 1}</Text>
          <Center padding={1}>
            {pnl['count']} Trade(s)
          </Center>
          <Center fontWeight='bold' isNumeric>
            {pnlValue(formatter.format(pnl['pnl']))}
          </Center>
      </GridItem>
    ));
    return content;
  }
  */
  
  
  const getPnlDays = () => {
    const firstDay = new Date(calYear, calMonth, 1).getDay();
    const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
    
    // Calculate the total number of days including the offset from the first day
    const totalDays = firstDay + daysInMonth;
    const numberOfWeeks = Math.ceil(totalDays / 7);
  
    // Initialize a 2D array to hold the days for each week
    let weeks = Array.from({ length: numberOfWeeks }, () => []);
  
    // Populate the weeks array with days
    for (let i = 0; i < daysInMonth; i++) {
      const dayOfWeek = (firstDay + i) % 7;
      const weekOfMonth = Math.floor((firstDay + i) / 7);
      weeks[weekOfMonth][dayOfWeek] = i + 1;
    }
  
    // Generate the content for each day, ensuring to skip the 6th week if it is empty
    let content = [];
    weeks.forEach((week, weekIndex) => {
      week.forEach((day, dayIndex) => {
        if (day) {
          const pnl = pnlYTD.months[calMonth][calMonth][day - 1];
          content.push(
            <GridItem
              key={`${weekIndex}-${dayIndex}`}
              boxShadow='inner'
              border='1px'
              borderColor='darkgray'
              rounded='md'
              p='1'
              w='100px'
              h='100%'
              _hover={{ bg: "gray.400" }}
              bg={colorChange(pnl['pnl'])}
              onClick={e => handleTradesOfDay(e, day)}
            >
              <Text fontWeight='bold'>{day}</Text>
              <Center padding={1}>
                {pnl['count']} Trade(s)
              </Center>
              <Center fontWeight='bold' isNumeric>
                {pnlValue(formatter.format(pnl['pnl']))}
              </Center>
            </GridItem>
          );
        }
      });
    });
  
    return content;
  }
  

  useEffect(() => {
    let year = calYear;
    if(user.user_id != undefined){
      dispatch(getPnlByYear({ year }));
    }
    setFilterTradeType('');
    setFilterSecurityType('');
    setFilterTickerName('');
    setSearchTickerValue('');
    setSelectedTickerValue('');
  }, [calYear, user]); 

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
              </Box>
                  <Button size="sm" backgroundColor='gray.300' width="full" color={colorMode === 'light' ? "none" : "gray.800"} onClick={handleSubmitFilter} >
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
      <Button ref={btnRef} colorScheme='white' onClick={e => setFilterDrawer(true)}>
       <Icon as={BsFilter} color='grey' size='lg'></Icon>
      </Button>
      </Box>
      {filterDrawer}
      <Drawer
        isOpen={filterDrawer}
        placement='left'
        onClose={e => setFilterDrawer(false)}
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
                {appliedFiltersComponent()}
          </DrawerBody>

          <DrawerFooter>
            <Button size="sm" backgroundColor='gray.300' width="full" color={colorMode === 'light' ? "none" : "gray.800"} onClick={handleSubmitFilter}>
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
    setFilterDrawer(false);
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
    let year = calYear;
    await dispatch(
      getPnlByYearFiltered({
        filters,
        year
      })
    );
    setFilters(filters);
    //setToggleFilter(!toggleFilter);
  }

  const handleClearFilter = async (e) => {
    e.preventDefault();
    setFilterDrawer(false);
    setFilterTradeType('');
    setFilterSecurityType('');
    setFilterTickerName('');
    setSearchTickerValue('');
    setSelectedTickerValue('');
    let year = calYear;
    await dispatch(getPnlByYear({ year }));
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
          
          <Box overflowX="auto" flexGrow="1" display="flex" borderWidth="1px" rounded="lg" alignItems="stretch">
          {authLoading && !tradesOfDayPopUp && !tradesOfWeekPopUp && !tradesOfMonthPopUp ?
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
              w='full'
              overflowX="auto"
            >
            {hasPnLInfo ? (
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
              overflowX="auto"
            >
              <HStack overflowX="auto" w='100%'>
                <Select w='150px' border='1px' borderColor='darkgray' size="md" variant='filled' onChange={(e) => setCalMonth(monthsString.indexOf(e.target.value))}>
                <option value="" disabled selected>{monthsString[calMonth]}</option>
                  {monthsString.map((mmonth) => (<option key={mmonth}>{mmonth}</option>))}
                </Select>
                <Select 
                w='100px' 
                size="md" 
                variant='filled' 
                border='1px' 
                borderColor='darkgray'
                onChange={(e) => {
                  setCalYear(e.target.value); 
                }}>
                  <option value="" disabled selected>{calYear}</option>
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
              <HStack spacing={8} overflowX="auto" w='100%'>
              <VStack
                spacing={4}
                align='stretch'
              >
              <Grid templateColumns='repeat(7, 1fr)' templateRows='repeat(1, 1fr)' gap={3}>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                    Sunday
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                    Monday
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                    Tuesday
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                    Wednesday
                  </Center>
                </GridItem>                
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                    Thursday
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                    Friday
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100px' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
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
              {tradesOfDayPopUp} ? (
              <AlertDialog
                motionPreset='slideInBottom'
                isOpen={tradesOfDayPopUp}
                leastDestructiveRef={cancelRef}
                onClose={e => handleCancelTradesOfDay(e)}
                isCentered={true}
                closeOnOverlayClick={true}
                size="xl"
              >
              {authLoading ?
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
                  <Center>
                    Trades Closed on {(new Date(calYear, calMonth, calDay)).toDateString()}
                  </Center>
                  </AlertDialogHeader>

                  <AlertDialogBody>
                  {hasTradesofDay ? (
                  <TableContainer overflowY="auto" maxHeight="300px" rounded="lg">
                    <Table size='sm' variant='striped' colorScheme={colorMode === 'light' ? 'whiteAlpha' : "gray.700"}>
                      <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"}>
                        <Tr>
                          <Th>Trade<br></br>Type</Th>
                          <Th>Security<br></br>Type</Th>
                          <Th>Ticker</Th>
                          <Th>PNL</Th>
                          <Th>% W/L</Th>
                        </Tr>
                      </Thead>
                          <Tbody>
                            {trades.trades.map((trades, index) => (
                              <Tr>
                                <Td>{trades.trade_type}</Td>
                                <Td>{trades.security_type}</Td>
                                <Td>{trades.ticker_name}</Td>
                                <Td isNumeric>{trades.pnl}</Td>
                                <Td isNumeric>{trades.percent_wl}</Td>
                              </Tr>
                            ))}
                          </Tbody>
                    </Table>
                  </TableContainer>
                  ) : (
                  <Center>
                    <Badge variant='subtle' colorScheme='red' fontSize='0.8em'>
                      No Trades Closed on This Day
                    </Badge>
                  </Center>
                  )}
                  </AlertDialogBody>

                  <AlertDialogFooter>
                  <Flex width="100%" justifyContent="space-between">
                    <Stat flex="1">
                      <StatLabel>Total Trades</StatLabel>
                      <StatNumber>{(pnlYTD.months[calMonth][calMonth][calDay-1]?.count ?? 0)}</StatNumber>
                    </Stat>
                    <Stat flex="1" textAlign="right">
                      <StatLabel>Total PnL</StatLabel>
                      <StatNumber color={colorChangeDay(pnlYTD.months[calMonth][calMonth][calDay-1]?.pnl ?? 0)}>{pnlValue(formatter.format(pnlYTD.months[calMonth][calMonth][calDay-1]?.pnl ?? 0))}</StatNumber>
                    </Stat>
                  </Flex>
                  </AlertDialogFooter>
                </AlertDialogContent>
                </AlertDialogOverlay>
              }
              </AlertDialog>
              )
              <VStack
                spacing={4}
                align='stretch'
                display='flex'
              >
              <Grid templateColumns='repeat(1, 1fr)' templateRows='repeat(1, 1fr)' gap={3}>
                <GridItem whiteSpace='nowrap' boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' w='100%' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
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
              {tradesOfWeekPopUp} ? (
              <AlertDialog
                motionPreset='slideInBottom'
                isOpen={tradesOfWeekPopUp}
                leastDestructiveRef={cancelRef}
                onClose={e => handleCancelTradesOfWeek(e)}
                isCentered={true}
                closeOnOverlayClick={true}
                size="xl"
              >
              {authLoading ?
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
                  <Center>
                    Trades Closed from {(new Date(calStartWeek)).toDateString()} to {(new Date(calEndWeek)).toDateString()}
                  </Center>
                  </AlertDialogHeader>

                  <AlertDialogBody>
                  {hasTradesofDay && hasStats ? (
                  <TableContainer overflowY="auto" maxHeight="300px" rounded="lg">
                    <Table size='sm' variant='striped' colorScheme={colorMode === 'light' ? 'whiteAlpha' : "gray.700"}>
                      <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"}>
                        <Tr>
                          <Th>Trade<br></br>Type</Th>
                          <Th>Security<br></br>Type</Th>
                          <Th>Ticker</Th>
                          <Th>PNL</Th>
                          <Th>% W/L</Th>
                        </Tr>
                      </Thead>
                          <Tbody>
                            {trades.trades.map((trades, index) => (
                              <Tr>
                                <Td>{trades.trade_type}</Td>
                                <Td>{trades.security_type}</Td>
                                <Td>{trades.ticker_name}</Td>
                                <Td isNumeric>{trades.pnl}</Td>
                                <Td isNumeric>{trades.percent_wl}</Td>
                              </Tr>
                            ))}
                          </Tbody>
                    </Table>
                  </TableContainer>
                  ) : (
                  <Center>
                    <Badge variant='subtle' colorScheme='red' fontSize='0.8em'>
                      No Trades Closed in This Week
                    </Badge>
                  </Center>
                  )}
                  </AlertDialogBody>

                  <AlertDialogFooter>
                  <Flex width="100%" justifyContent="space-between">
                    <Stat flex="1">
                      <StatLabel>Total Trades</StatLabel>
                      <StatNumber>{(trades?.stats?.num_trades ?? 0)}</StatNumber>
                    </Stat>
                    <Stat flex="1" textAlign="right">
                      <StatLabel>Total PnL</StatLabel>
                      <StatNumber color={colorChangeDay(trades?.stats?.total_pnl ?? 0)}>{pnlValue(formatter.format(trades?.stats?.total_pnl ?? 0))}</StatNumber>
                    </Stat>
                  </Flex>
                  </AlertDialogFooter>
                </AlertDialogContent>
                </AlertDialogOverlay>
              }
              </AlertDialog>
              )
              <HStack spacing={8} overflowX="auto" w='100%'>
              <Grid overflowX='scroll' templateColumns='repeat(6, 1fr)' gap={6}>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' minWidth='150px' maxWidth='150px' w='100%' h='100%'  _hover={{ bg: "gray.400" }} bg={colorChange(getMonthlyTotal())} onClick={e => handleTradesOfMonth(e)}>
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>Monthly PnL</StatLabel>
                    <StatNumber>{pnlValue(formatter.format(getMonthlyTotal()))}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <AlertDialog
                  motionPreset='slideInBottom'
                  isOpen={tradesOfMonthPopUp}
                  leastDestructiveRef={cancelRef}
                  onClose={e => handleCancelTradesOfMonth(e)}
                  isCentered={true}
                  closeOnOverlayClick={true}
                  size="xl"
                >
                {authLoading ?
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
                    <Center>
                      Trades Closed in {monthsString[calMonth]}
                    </Center>
                    </AlertDialogHeader>

                    <AlertDialogBody>
                    {hasTradesofDay && hasStats ? (
                    <TableContainer overflowY="auto" maxHeight="300px" rounded="lg">
                      <Table size='sm' variant='striped' colorScheme={colorMode === 'light' ? 'whiteAlpha' : "gray.700"}>
                        <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"}>
                          <Tr>
                            <Th>Trade<br></br>Type</Th>
                            <Th>Security<br></br>Type</Th>
                            <Th>Ticker</Th>
                            <Th>PNL</Th>
                            <Th>% W/L</Th>
                          </Tr>
                        </Thead>
                            <Tbody>
                              {trades.trades.map((trades, index) => (
                                <Tr>
                                  <Td>{trades.trade_type}</Td>
                                  <Td>{trades.security_type}</Td>
                                  <Td>{trades.ticker_name}</Td>
                                  <Td isNumeric>{trades.pnl}</Td>
                                  <Td isNumeric>{trades.percent_wl}</Td>
                                </Tr>
                              ))}
                            </Tbody>
                      </Table>
                    </TableContainer>
                    ) : (
                    <Center>
                      <Badge variant='subtle' colorScheme='red' fontSize='0.8em'>
                        No Trades Closed in This Month
                      </Badge>
                    </Center>
                    )}
                    </AlertDialogBody>

                    <AlertDialogFooter>
                    <Flex width="100%" justifyContent="space-between">
                      <Stat flex="1">
                        <StatLabel>Total Trades</StatLabel>
                        <StatNumber>{(trades?.stats?.num_trades ?? 0)}</StatNumber>
                      </Stat>
                      <Stat flex="1" textAlign="right">
                        <StatLabel>Total PnL</StatLabel>
                        <StatNumber color={colorChangeDay(trades?.stats?.total_pnl ?? 0)}>{pnlValue(formatter.format(trades?.stats?.total_pnl ?? 0))}</StatNumber>
                      </Stat>
                    </Flex>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                  </AlertDialogOverlay>
                }
                </AlertDialog>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' minWidth='150px' maxWidth='150px' w='100%' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># Green Days</StatLabel>
                    <StatNumber>{getGreenDayTotal()}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' minWidth='150px' maxWidth='150px' w='100%' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel># Red Days</StatLabel>
                    <StatNumber>{getRedDayTotal()}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' minWidth='150px' maxWidth='150px' w='100%' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>% Green Days</StatLabel>
                    <StatNumber>{percent.format(getGreenDayPercent())}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' minWidth='150px' maxWidth='150px' w='100%' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>% Red Days</StatLabel>
                    <StatNumber>{percent.format(getRedDayPercent())}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
                <GridItem boxShadow='inner' border='1px' borderColor='darkgray' rounded='md' p='1' minWidth='150px' maxWidth='150px' w='100%' h='100%' bg={colorMode === 'light' ? "gray.100" : "gray.700"} >
                  <Center fontWeight='bold'>
                  <Stat>
                    <StatLabel>% Break Even Days</StatLabel>
                    <StatNumber>{percent.format(getBreakevenDayPercent())}</StatNumber>
                  </Stat>
                  </Center>
                </GridItem>
              </Grid>
              </HStack>
            </VStack>
            ) : (
              <Text>
              No PnL Info
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

