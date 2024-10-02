import React, { useEffect, useState } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades, getTradesFiltered , getTradesPage, expiredLogout} from '../store/auth'
import { Link as RouterLink, useNavigate, useLocation} from "react-router-dom";
import '../styles/summary.css';
import '../styles/logtrade.css';
import '../styles/filter.css';
import moment from 'moment'; 
import 'moment-timezone';
import { BsFilter } from "react-icons/bs";
import axios from "axios";
import { VscTriangleLeft, VscTriangleRight } from "react-icons/vsc";
import { IoFilter } from "react-icons/io5";
import {
  Flex,
  IconButton,
  Text,
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
  Center,
  Divider,
  UnorderedList,
  ListItem,
  Spinner,
  Icon,
  Heading,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useDisclosure,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  Input,
  useColorMode,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  Textarea,
  Select,
  Toast,
  useToast,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  chakra,
  Box,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
  ButtonGroup,
  Badge,
  HStack,
  VStack,
  OrderedList
} from "@chakra-ui/react";
import { TriangleDownIcon, TriangleUpIcon } from '@chakra-ui/icons';
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { update, getTrade, reset, deleteTrade, searchTicker, importCsv, exportCsv, updateTrades, bulkUpdateCsv } from '../store/trade';


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

export default function Summary({ user }) {
  const btnRef = React.useRef()
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const query = useQuery();
  const { trade } = useSelector((state) => state.trade);
  const { success } = useSelector((state) => state.trade);
  const { trades } = useSelector((state) => state.auth);
  const tradeError = useSelector((state) => state.trade.error);
  const tradeInfo = useSelector((state) => state.trade.info);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const hasTrades = ((trades && trades.trades && Object.keys(trades.trades).length > 0) ? (true):(false));
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false));
  const hasTrade = ((trade && Object.keys(trade).length > 2) ? (true):(false));

  const [editTrade, setEditTrade] = useState(false);
  const [bulkUpdateWithCSV, setBulkUpdateWithCSV] = useState(false);
  const [toggleFilter, setToggleFilter] = useState(false);

  const [filterDrawer, setFilterDrawer] = useState(false);

  const [visib, setVisib] = useState(false);
  function checkVisbility(tradePayload){
    setVisib(tradePayload.security_type === "Options");
  }

  const { tickerNameSearch } = useSelector((state) => state.trade);

  const user_id = user.user_id;

  const [filters, setFilters] = useState({});

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
    const savedSummaryFilters = window.localStorage.getItem('SummaryFilters');
    if (savedSummaryFilters) {
      const SummaryFilters = JSON.parse(savedSummaryFilters);
      setFilterTradeType(SummaryFilters.trade_type || "");
      setFilterSecurityType(SummaryFilters.security_type || "");
      setFilterTickerName(SummaryFilters.ticker_name || "");
      setSelectedTickerValue(SummaryFilters.ticker_name || "");
      setFilterFromDate(SummaryFilters.from_date || "");
      setFilterToDate(SummaryFilters.to_date || "");
      setFilters(SummaryFilters);
    }
  }, []); // Empty dependency array means this runs once on mount


  const [page, setPage] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [numRows, setNumRows] = useState(0);
  const [num_results, setNumResults] = useState(100);
  const pageStartOffset = (page !== 0) ? ((page*numRows)-(numRows-1)) : 0;
  const pageEndOffset = totalCount < (page*numRows) ? totalCount : (page*numRows);
  const [backPageEnable, setBackPageEnable] = useState(false);
  const [nextPageEnable, setNextPageEnable] = useState(false);

  useEffect(() => {
    if (hasTrades) {
      setPage(parseInt(trades.page));
      setTotalCount(parseInt(trades.count));
      setNumRows(parseInt(trades.numrows));
    } else if (trades && 'count' in trades && trades.count === 0){
      setPage(trades.page);
      setTotalCount(trades.count);
      setNumRows(trades.numrows);
    }
  }, [trades]); 

  useEffect(() => {
    if (hasTrade && 'rr' in trade && trade.rr != null) {
      setRisk(trade.rr.split(":")[0] || '1');
      setReward(trade.rr.split(":")[1] || '1');
    }
  }, [trade]); 

  const [trade_id, setTradeID] = useState(null);

  const [trade_type, setTradeType] = useState("");
  const [security_type, setSecurityType] = useState("");
  const [ticker_name, setTickerName] = useState("");
  const [trade_date, setTradeDate] = useState("");
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
  const [filter_from_date, setFilterFromDate] = useState("");
  const [filter_to_date, setFilterToDate] = useState("");

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }

  const today = returnInTZ(new Date().toISOString());

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();
  const [deletealertdialog, setDeleteAlertDialog] = useState(false);

  const authLoading = useSelector((state) => state.auth.loading);
  const tradeLoading = useSelector((state) => state.trade.loading);

  const [exportLoading, setExportLoading] = useState(false);

  const [editLoading, setEditLoading] = useState(false);

  const [editButtonInstance, setEditButtonInstance] = useState(null);

  const [importCsvDialog, setImportDialog] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const [selectedRow, setSelectedRow] = useState([]);
  const [trade_ids, setSelectedTradeIds] = useState([]);

  const { colorMode, toggleColorMode } = useColorMode();

  const [searchValue, setSearchValue] = useState('');
  const [searchTickerValue, setSearchTickerValue] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchTickerResults, setSearchTickerResults] = useState([]);
  const [selectedValue, setSelectedValue] = useState('');
  const [selectedTickerValue, setSelectedTickerValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const format = (val1,val2) => val1 + ":" + val2;
  const [risk, setRisk] = useState("1");
  const [reward, setReward] = useState("1");

  useEffect(() => {
    if(risk > 0 && reward > 0 && rr !== format(risk, reward)){
      setRR(format(risk,reward));
    }
  }, [risk, reward]); 

  useEffect(() => {
    if (rr && rr !== format(risk, reward)) {
      const [riskValue, rewardValue] = rr.split(':').map(val => parseInt(val));
      setRisk(riskValue);
      setReward(rewardValue);
    }
  }, [rr]);

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

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  useEffect(() => {
    evaluatePage();
  }, [page,totalCount,num_results,numRows]);

  const evaluateSuccess = async () => {
    if(success === true && trade && trade.result === "Trade Edited Successfully"){
      setEditTrade(false);
      setToastMessage(trade.result);
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
      if(filter_from_date !== '' || filter_to_date !== ''){
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
      filters.numrows = num_results;
      await dispatch(getTradesPage({ filters }));
      dispatch(
        reset()      
      );
      handleFilterChange(filtersToQueryString(filters));
      window.localStorage.setItem('SummaryFilters', JSON.stringify(filters));
      clearFormStates();
      setSelectedRow([]);
      setTradeID(null);
      setSearchValue('');
      setIsDropdownOpen(false);
    }
    if(success === true && trade && trade.result && trade.result.includes("Trades Updated Successfully")){
      setEditTrade(false);
      setToastMessage(trade.result);
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
      if(filter_from_date !== '' || filter_to_date !== ''){
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
      filters.numrows = num_results;
      await dispatch(getTradesPage({ filters }));
      dispatch(
        reset()      
      );
      handleFilterChange(filtersToQueryString(filters));
      window.localStorage.setItem('SummaryFilters', JSON.stringify(filters));
      clearFormStates();
      setSelectedRow([]);
      setTradeID(null);
      setSearchValue('');
      setIsDropdownOpen(false);
    }
    if(success === true && trade && trade.result === "Trade Successfully Deleted"){
      setToastMessage(trade.result);
    }
    if(success === true && trade && trade.result === "Trades Successfully Deleted"){
      setToastMessage(trade.result);
    }
    if(success === true && trade && trade.result === "Trades Imported Successfully"){
      setToastMessage(trade.trades.length.toString() + " " + trade.result);
    }
    if(success === true && trade && trade.result && trade.result.includes("Trades Updates Imported Successfully")){
      let toast_message = trade.updated_ids.length.toString() + " " + trade.result;
      if(trade && trade.error_ids && trade.error_ids.length > 0){
        //toast_message += "\nSome Errors Present, Downloading Errors...";
        setToastErrorMessage("Some Errors Present, Downloading Errors...");
      }
      setToastMessage(toast_message);
      dispatch(
        reset()      
      );
    }
    if(success === true && trade && trade.result === "Trades Exported Successfully"){
      setToastMessage(trade.result);
    }
  }

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

  useEffect(() => {
    evaluateError();
  }, [error, tradeError]); 

  const evaluateError = () => {
    if(error === true){
      setToastErrorMessage(info.response.data.result);
    }
    if(tradeError === true){
      setToastErrorMessage(tradeInfo.response.data.result);
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

  useEffect(() => {
    const savedUpdateTradeInfo = window.localStorage.getItem('updateTradeInfo');
    const savedUpdateBulkTradeInfo = window.localStorage.getItem('updateBulkTradeInfo');
    if (savedUpdateTradeInfo) {
      const updateTradeInfo = JSON.parse(savedUpdateTradeInfo);
      setTradeType(updateTradeInfo.trade_type || "");
      setSecurityType(updateTradeInfo.security_type || "");
      setTickerName(updateTradeInfo.ticker_name || "");
      setTradeDate(updateTradeInfo.trade_date || "");
      setExpiry(updateTradeInfo.expiry || "");
      setStrike(updateTradeInfo.strike || "");
      setBuyValue(updateTradeInfo.buy_value || "");
      setUnits(updateTradeInfo.units || "");
      setRR(updateTradeInfo.rr || "");
      setPNL(updateTradeInfo.pnl || "");
      setPercentWL(updateTradeInfo.percent_wl || "");
      setComments(updateTradeInfo.comments || "");
      // Clear the saved info after loading it
      //window.localStorage.removeItem('userInfo');
    }
    if (savedUpdateBulkTradeInfo) {
      const updateBulkTradeInfo = JSON.parse(savedUpdateBulkTradeInfo);
      setTradeType(updateBulkTradeInfo.trade_type || "");
      setSecurityType(updateBulkTradeInfo.security_type || "");
      setTickerName(updateBulkTradeInfo.ticker_name || "");
      setTradeDate(updateBulkTradeInfo.trade_date || "");
      setExpiry(updateBulkTradeInfo.expiry || "");
      setStrike(updateBulkTradeInfo.strike || "");
      setBuyValue(updateBulkTradeInfo.buy_value || "");
      setUnits(updateBulkTradeInfo.units || "");
      setRR(updateBulkTradeInfo.rr || "");
      setPNL(updateBulkTradeInfo.pnl || "");
      setPercentWL(updateBulkTradeInfo.percent_wl || "");
      setComments(updateBulkTradeInfo.comments || "");
      // Clear the saved info after loading it
      //window.localStorage.removeItem('userInfo');
    }
  }, []); // Empty dependency array means this runs once on mount

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
    setRisk(hasTrade && 'rr' in trade && trade.rr != null ? trade.rr.split(":")[0] : "1");
    setReward(hasTrade && 'rr' in trade && trade.rr != null ? trade.rr.split(":")[1] : "1");
    window.localStorage.removeItem('updateTradeInfo');
    window.localStorage.removeItem('updateBulkTradeInfo');
  }

  const keysToSkip = ['page', 'numrows'];
  
  const appliedFilters = Object.entries(filters).filter(([key]) => !keysToSkip.includes(key)).map(([key, value]) => (
    <Tr key={key}>
      <Td>{key}</Td>
      <Td>{value}</Td>
    </Tr>
  ));


  const appliedFiltersComponent = () => {
    let content = [];
    if(Object.keys(filters).length !== 0 && Object.keys(filters).some(key => ['trade_type','security_type','ticker_name','from_date','to_date'].includes(key))){
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
    if (choiceOptions.value === "" && trade && trade.security_type && trade.security_type === "Options"){
      setVisib(true);
      setExpiry("");
      setStrike("");
    }else if (choiceOptions.value === "" && trade && trade.security_type && trade.security_type === "Shares"){
      setVisib(false);
      setExpiry("");
      setStrike("");
    }
  }

  const handleGotoEdit = async (e) => {
    e.preventDefault();
    if (selectedRow.length === 1){
      setEditLoading(true);
      setEditButtonInstance(selectedRow);
      const res = await dispatch(
        getTrade({
          trade_id
        })
      );
      checkVisbility(res.payload);
      setTradeID(trade_id);
      setEditTrade(true);
      setEditLoading(false);
    } else if (selectedRow.length > 1){
      setSelectedTradeIds(selectedRow.map(index => trades.trades[index].trade_id));
      setEditTrade(true);
      //set trade ids like delete trades - DONE
      //logic in html to look at selected rows length - DONE
      //html for this update trades bulk update - DONE
      //API call logic - DONE
      //API in store file - DONE
      //Handle API response - DONE
      //Caching stuff - DONE
    }
    
  };

  const getBulkUpdateCSVComponent = () => {
    let content = [];
    content.push(
      <>
      <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>CSV Bulk Update</Heading>
        <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="scroll" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          <VStack overflow="scroll">
          <Stack
                spacing={4}
                p="1rem"
                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "whiteAlpha.100"}
                boxShadow="md"
              >
            <HStack fontSize='lg' fontWeight='bold'>
              <Text>
                Instructions
              </Text>
            </HStack>
            <HStack>
              <OrderedList spacing={2} paddingTop={2}>
                <ListItem>Export desired trades from Summary Table</ListItem>
                <ListItem>Make necessary changes to each trade entry</ListItem>
                <ListItem>*If you are clearing any columns, make the value None*</ListItem>
                <ListItem>Delete any rows you are not making changes to</ListItem>
                <ListItem>Add CSV file below and click submit</ListItem>
              </OrderedList>
            </HStack>
            <Text paddingTop={5} paddingBottom={4}>Heres an example to show a file thats ready for import:{' '} 
              <Link href="./csv/bulk_update_example.csv" download="example_bulk_trade_updates.csv" color='blue.500'>Download Example</Link>
            </Text>
            <HStack>
              <Input
                paddingTop={1}
                type="file"
                id="file"
                accept=".csv" 
                maxWidth="400px"
                ml={3}
                onChange={handleFileInputChange}/>
            {tradeLoading ? <Text paddingLeft={3} color='red.500'>Loading your Trades...</Text> : ( <Text></Text>) }
            </HStack>
            <Flex justifyContent="flex-end">
            <HStack paddingTop={10} >
              <Button ref={cancelRef} minWidth='100px' onClick={e => handleCancelBulkUpdateCsv(e)}>
                Cancel
              </Button>
              {tradeLoading ?
                <Button colorScheme='blue' minWidth='100px' ml={3}>
                  <Center>
                    <Spinner
                      thickness='2px'
                      speed='0.65s'
                      emptyColor='gray.200'
                      color='grey.500'
                      size='sm'
                    />
                  </Center>
                </Button>
              :
                <Button colorScheme='blue' minWidth='100px' isDisabled={!selectedFile} onClick={e => handleConfirmBulkUpdateCsv(e)} ml={3}>
                  Submit
                </Button>
              } 
            </HStack>
            </Flex>
          </Stack>
          </VStack>
        </Box>
      </>
    );
    return content
  }

  const getEditComponent = () => {
    let content = [];
    if (selectedRow.length === 1){
      content.push(
        <>
        <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>Update Trade</Heading>
        <Box minW={{ base: "90%", md: "468px" }} maxW="650px" rounded="lg" overflow="hidden" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          {tradeLoading ? 
            <Stack
                spacing={4}
                p="1rem"
                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "whiteAlpha.100"}
                boxShadow="md"
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
          <form>
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "whiteAlpha.100"}
              boxShadow="md"
            >
              <Box display="flex">
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select value={trade_type} onChange={(e) => setTradeType(e.target.value)}>
                    <option value="" disabled selected>{trade.trade_type}</option>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select id="optionsSelection" value={security_type} onChange={(e) => {changeShowOptions(e.target.value); setSecurityType(e.target.value);}}>
                    <option value="" disabled selected>{trade.security_type}</option>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <div class="ticker-search">
                    <Input type="text" placeholder={trade.ticker_name} value={selectedValue ? selectedValue : searchValue} onChange={handleInputChange} onClick={handleInputClick}/>
                    {isDropdownOpen && (
                      <ul class={colorMode === 'light' ? "search-dropdown" : "search-dropdowndark"}>
                        {isLoading ? (
                          <div>Loading...</div>
                        ) : (
                          searchResultItems
                        )}
                      </ul>
                    )}
                  </div>
                </FormControl>
              </Box>
              
              <Box style={{display: visib ? "flex" : "none"}}>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Expiry (Options Only) *
                </FormHelperText>
                <Input
                    value={expiry}
                    placeholder={trade.expiry}
                    onFocus={(e) => (e.target.type = "date")}
                    onBlur={(e) => (e.target.type = "text")}
                    max="3900-12-31"
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
                    value={strike}
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
                  Date Trade was Closed *
                </FormHelperText>
                <Input
                    value={trade_date}
                    placeholder={trade.trade_date}
                    onFocus={(e) => (e.target.type = "date")}
                    onBlur={(e) => (e.target.type = "text")}
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
                    placeholder={trade.buy_value}
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
                    placeholder={trade.units}
                    onChange={(e) => setUnits(e.target.value)}
                  />
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Risk/Reward Ratio (R:R) *
                  </FormHelperText>
                  <HStack>
                  <NumberInput
                    value={risk}
                    onChange={(stringValue) => setRisk(stringValue)}
                    //defaultValue = {trade.rr.split(":")[0]}
                    min={1}
                    max={200}
                    inputMode='text'
                  >
                    <NumberInputField />
                    <NumberInputStepper>
                      <NumberIncrementStepper />
                      <NumberDecrementStepper />
                    </NumberInputStepper>
                  </NumberInput>
                  <Text>
                    :
                  </Text>
                  <NumberInput
                    value={reward}
                    onChange={(stringValue) => setReward(stringValue)}
                    //defaultValue = {trade.rr.split(":")[1]}
                    min={1}
                    max={200}
                    inputMode='text'
                  >
                    <NumberInputField />
                    <NumberInputStepper>
                      <NumberIncrementStepper />
                      <NumberDecrementStepper />
                    </NumberInputStepper>
                  </NumberInput>
                  </HStack>
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    PNL *
                  </FormHelperText>
                  <Input
                    value={pnl}
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
                    value={percent_wl}
                    type="name"
                    readOnly
                    placeholder={trade.percent_wl}
                    defaultValue={percent_wl}
                  />
              </FormControl>
              </Box>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Comments *
                  </FormHelperText>
                  <Textarea value={comments} placeholder={trade.comments} onChange={(e) => setComments(e.target.value)}/>
              </FormControl>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleDoneEdit}
              >
                Update
              </Button>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleClear}
              >
                Clear
              </Button>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="gray"
                width="full"
                onClick={handleCancel}
              >
                Cancel
              </Button>
            </Stack>
          </form>
        }
        </Box>
        </>
      );
    }else if (selectedRow.length > 1){
      content.push(
        <>
        <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>Bulk Update Trades</Heading>
        <Box minW={{ base: "90%", md: "468px" }} maxW="650px" rounded="lg" overflow="hidden" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          {tradeLoading ? 
            <Stack
                spacing={4}
                p="1rem"
                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "whiteAlpha.100"}
                boxShadow="md"
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
          <form>
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "whiteAlpha.100"}
              boxShadow="md"
            >
              <Box display="flex">
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select value={trade_type} placeholder='Select Trade Type' onChange={(e) => setTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select id="optionsSelection" value={security_type} placeholder='Select Security Type' onChange={(e) => {changeShowOptions(e.target.value); setSecurityType(e.target.value)}}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <div class="ticker-search">
                    <Input type="text" value={selectedValue ? selectedValue : searchValue} onChange={handleInputChange} onClick={handleInputClick}/>
                    {isDropdownOpen && (
                      <ul class={colorMode === 'light' ? "search-dropdown" : "search-dropdowndark"}>
                        {isLoading ? (
                          <div>Loading...</div>
                        ) : (
                          searchResultItems
                        )}
                      </ul>
                    )}
                  </div>
                </FormControl>
              </Box>
              
              <Box style={{display: visib ? "flex" : "none"}}>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Expiry (Options Only) *
                </FormHelperText>
                <Input
                    value={expiry}
                    type="date"
                    max="3900-12-31"
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
                    value={strike}
                    type="name"
                    onChange={(e) => setStrike(e.target.value)}
                  />
                </InputGroup>
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Date Trade was Closed *
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
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Risk/Reward Ratio (R:R) *
                  </FormHelperText>
                  <HStack>
                  <NumberInput
                    onChange={(stringValue) => setRisk(stringValue)}
                    value = {risk}
                    min={1}
                    max={200}
                    inputMode='text'
                  >
                    <NumberInputField />
                    <NumberInputStepper>
                      <NumberIncrementStepper />
                      <NumberDecrementStepper />
                    </NumberInputStepper>
                  </NumberInput>
                  <Text>
                    :
                  </Text>
                  <NumberInput
                    onChange={(stringValue) => setReward(stringValue)}
                    value = {reward}
                    min={1}
                    max={200}
                    inputMode='text'
                  >
                    <NumberInputField />
                    <NumberInputStepper>
                      <NumberIncrementStepper />
                      <NumberDecrementStepper />
                    </NumberInputStepper>
                  </NumberInput>
                  </HStack>
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
              </Box>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Comments *
                  </FormHelperText>
                  <Textarea value={comments} placeholder='Reflect on your Trade...' onChange={(e) => setComments(e.target.value)}/>
              </FormControl>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme='blue'
                width="full"
                onClick={handleDoneEditBulk}
              >
                Update
              </Button>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleGoToCSVUpdate}
              >
                Update w/ CSV
              </Button>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleClear}
              >
                Clear
              </Button>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="gray"
                width="full"
                onClick={handleCancel}
              >
                Cancel
              </Button>
            </Stack>
          </form>
        }
        </Box>
        </>
      );
    }
    return content
  };

  const handleExport = async (e) => {
    setExportLoading(true);
    const exported_trades = trades.trades
    const res = await dispatch(
      exportCsv({
        exported_trades
      })
    );
    const csvData = res.payload;
    // Create a downloadable link in the client's browser
    const downloadLink = document.createElement('a');
    downloadLink.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvData);
    downloadLink.download = 'trades.csv';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    setExportLoading(false);
  };


  const handleDeleteButton = (e) => {
    setSelectedTradeIds(selectedRow.map(index => trades.trades[index].trade_id));
    setDeleteAlertDialog(true);
    onOpen();
  };

  const handleConfirmDelete = async (e) => {
    e.preventDefault();
    await dispatch(
      deleteTrade({
        trade_ids
      })
    );
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
    if(filter_from_date !== '' || filter_to_date !== ''){
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
    filters.numrows = num_results;
    await dispatch(getTradesPage({ filters }));
    handleFilterChange(filtersToQueryString(filters));
    window.localStorage.setItem('SummaryFilters', JSON.stringify(filters));
    dispatch(
      reset()      
    );
    setSelectedTradeIds([]);
    setSelectedRow([]);
    setDeleteAlertDialog(false);
    onClose();
  };

  const handleCancelDelete = (e) => {
    setDeleteAlertDialog(false);
    onClose();
  };


  const handleDoneEdit = async (e) => {
    e.preventDefault();
    const updateTradeInfo = {
      trade_id,
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
    };
    await dispatch(
        update({
          trade_id,
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
        })
      );
    window.localStorage.setItem('updateTradeInfo', JSON.stringify(updateTradeInfo));
  };

  const handleDoneEditBulk = async (e) => {
    e.preventDefault();
    const ids = trade_ids;
    const updateBulkTradeInfo = {
      trade_ids,
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
    };
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
    window.localStorage.setItem('updateBulkTradeInfo', JSON.stringify(updateBulkTradeInfo));
  };

  const handleCancel = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    setEditTrade(false);
    clearFormStates();
    setSelectedRow([]);
    setTradeID(null);
    setIsLoading(false);
    setSearchValue('');
    setIsDropdownOpen(false);
  }

  const handleGoToCSVUpdate = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    setEditTrade(false);
    clearFormStates();
    setSelectedRow([]);
    setTradeID(null);
    setIsLoading(false);
    setSearchValue('');
    setIsDropdownOpen(false);
    setBulkUpdateWithCSV(true);
  }

  const handleCancelBulkUpdateCsv = (e) => {
    setBulkUpdateWithCSV(false);
  }

  const handleClear = (e) => {
    e.preventDefault();
    clearFormStates();
    setIsLoading(false);
    setSearchValue('');
    setIsDropdownOpen(false);
    changeShowOptions(e);
  }

  const handleNextPage = async (e) => {
    if(nextPageEnable){
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
      if(filter_from_date !== '' || filter_to_date !== ''){
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
      await dispatch(getTradesPage({ filters }));
      handleFilterChange(filtersToQueryString(filters));
      window.localStorage.setItem('SummaryFilters', JSON.stringify(filters));
      setSelectedRow([]);
    }
  }

  const handleBackPage = async (e) => {
    if(backPageEnable){
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
      if(filter_from_date !== '' || filter_to_date !== ''){
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
      await dispatch(getTradesPage({ filters }));  
      handleFilterChange(filtersToQueryString(filters));
      window.localStorage.setItem('SummaryFilters', JSON.stringify(filters));
      setSelectedRow([]);
    }
  }

  const handleChangeNumResults = async (e) => {
    const new_num_results = e.target.value;
    setNumResults(new_num_results);
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
    if(filter_from_date !== '' || filter_to_date !== ''){
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
    await dispatch(getTradesPage({ filters }));  
    handleFilterChange(filtersToQueryString(filters));
    window.localStorage.setItem('SummaryFilters', JSON.stringify(filters));
    setSelectedRow([]);
  }

  const handleInputTickerFIlterClick = (event) => {
    setIsDropdownOpen(!isDropdownOpen);
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
                    From Date
                  </FormHelperText>
                  <Input
                    value={filter_from_date}
                    type="date"
                    max={maxDate}
                    min="1900-01-01"
                    onChange={(e) => setFilterFromDate(e.target.value)}
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
    if(filter_from_date !== '' || filter_to_date !== ''){
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
    filters.numrows = num_results;
    await dispatch(getTradesPage({ filters })); 
    handleFilterChange(filtersToQueryString(filters));
    window.localStorage.setItem('SummaryFilters', JSON.stringify(filters)); 
    setSelectedRow([]);
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
    setFilterFromDate('');
    setFilterToDate('');
    const filters = {};
    filters.page = 1;
    filters.numrows = num_results;
    await dispatch(getTradesPage({ filters }));
    handleFilterChange(filtersToQueryString({}));
    window.localStorage.removeItem('SummaryFilters');
    setFilters({});
    setSelectedRow([]);
    //setToggleFilter(!toggleFilter);
  }

  const handleLogTrade = (e) => {
    navigate("/logTrade");
  }

  useEffect(() => {
    calculatePercent();
  }, [pnl, buy_value, units]); 

  const calculatePercent = () => {
    const pnlFloat=parseFloat(pnl);
    const buyValueFloat=parseFloat(buy_value);
    const unitsFloat=parseFloat(units);
    if (!isNaN(pnlFloat) && !isNaN(buyValueFloat) && buyValueFloat !== 0 && !isNaN(unitsFloat) && unitsFloat !== 0) {
      setPercentWL(((pnlFloat/(buyValueFloat*unitsFloat))*100).toFixed(2));
    }else if (!isNaN(pnlFloat) && isNaN(buyValueFloat && !isNaN(trade?.buy_value)) && !isNaN(unitsFloat) && unitsFloat !== 0){
      setPercentWL(((pnlFloat/(trade.buy_value*unitsFloat))*100).toFixed(2));
    }else if (isNaN(pnlFloat) && !isNaN(buyValueFloat) && buyValueFloat !== 0 && !isNaN(unitsFloat) && unitsFloat !== 0 && !isNaN(trade?.pnl)){
      setPercentWL(((trade.pnl/(buyValueFloat*unitsFloat))*100).toFixed(2));
    }else if (!isNaN(pnlFloat) && isNaN(buyValueFloat && !isNaN(trade?.buy_value)) && isNaN(unitsFloat) && !isNaN(trade?.units)){
      setPercentWL(((pnlFloat/(trade.buy_value*trade.units))*100).toFixed(2));
    }else if (isNaN(pnlFloat) && !isNaN(buyValueFloat) && buyValueFloat !== 0 && isNaN(unitsFloat) && !isNaN(trade?.units) && !isNaN(trade?.pnl)){
      setPercentWL(((trade.pnl/(buyValueFloat*trade.units))*100).toFixed(2));
    }else if (isNaN(pnlFloat) && isNaN(buyValueFloat && !isNaN(trade?.buy_value)) && !isNaN(unitsFloat) && unitsFloat !== 0 && !isNaN(trade?.pnl)){
      setPercentWL(((trade.pnl/(trade.buy_value*unitsFloat))*100).toFixed(2));
    }else if (!isNaN(pnlFloat) && !isNaN(buyValueFloat) && buyValueFloat !== 0 && isNaN(unitsFloat) && !isNaN(trade?.units)){
      setPercentWL(((pnlFloat/(buyValueFloat*trade.units))*100).toFixed(2));
    }else{
      setPercentWL("");
    }
  }

  const handleImportButton = (e) => {
    setImportDialog(true);
  };

  const handleCancelImportCsv = (e) => {
    setImportDialog(false);
    setSelectedFile(null);
  };

  const handleFileInputChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
    } else {
      setSelectedFile(null);
      alert("Please select a CSV file.");
    }
  };

  const handleConfirmImportCsv = async (e) => {
    await dispatch(
      importCsv({
        selectedFile
      })
    );
    setImportDialog(false);
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
    if(filter_from_date !== '' || filter_to_date !== ''){
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
    filters.numrows = num_results;
    await dispatch(getTradesPage({ filters }));
    handleFilterChange(filtersToQueryString(filters));
    window.localStorage.setItem('SummaryFilters', JSON.stringify(filters)); 
    setSelectedFile(null);
  };

  const downloadErrorCsv = (errorIds) => {
    // Define CSV headers with trade_id first
    const headers = ['trade_id', 'error_message'];
  
    // Function to properly escape any field with commas
    const escapeCsvField = (field) => {
      // Add double quotes around the field if it contains a comma
      return field.includes(',') ? `"${field}"` : field;
    };
  
    // Create CSV content with trade_id first and error_message second
    const csvContent = [
      headers.join(','),  // CSV headers as the first row
      ...errorIds.map(row => 
        [
          row.trade_id,  // trade_id comes first
          escapeCsvField(row.error_message)  // error_message comes second
        ].join(',')
      )  // Map each errorId into a row and handle comma escaping
    ].join('\n');  // Join each row with a newline
  
    // Create a blob from the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv' });
  
    // Create a temporary link to trigger file download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'errors.csv';  // Filename for the downloaded CSV
    document.body.appendChild(a);
    a.click();
    a.remove();  // Clean up the link after triggering the download
  };

  const handleConfirmBulkUpdateCsv = async (e) => {
    const res = await dispatch(
      bulkUpdateCsv({
        selectedFile
      })
    );
    const data = await res.payload;
      
    // Set the error IDs from the response
    const error_ids = (data.error_ids);
    // Automatically download CSV if there are error IDs
    if (data.error_ids && data.error_ids.length > 0) {
      downloadErrorCsv(data.error_ids);
    }
    setImportDialog(false);
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
    if(filter_from_date !== '' || filter_to_date !== ''){
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
    filters.numrows = num_results;
    await dispatch(getTradesPage({ filters }));
    handleFilterChange(filtersToQueryString(filters));
    window.localStorage.setItem('SummaryFilters', JSON.stringify(filters)); 
    setSelectedFile(null);
    setBulkUpdateWithCSV(false);
  };

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


  useEffect(() => {
    const fetchSearchResults = async () => {
      setIsLoading(true);
      const response = await axios.get(`https://ticker-2e1ica8b9.now.sh/keyword/${searchValue}`);
      const topResults = response.data.map(f => [f.symbol + ", " + f.name]);
      setSearchResults(topResults);
      setIsLoading(false);
    };

    if (searchValue) {
      fetchSearchResults();
      setIsDropdownOpen(true);
    } else {
      setSearchResults([]);
      setIsDropdownOpen(false);
    }
  }, [searchValue]);

  const handleInputChange = (event) => {
    setSelectedValue('');
    setSearchValue(event.target.value);
    setTickerName(event.target.value);
  };

  const handleInputClick = (event) => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleInputTickerFilterChange = (event) => {
    setSelectedTickerValue('');
    setSearchTickerValue(event.target.value);
    setFilterTickerName(event.target.value);
  };


  const handleSelection = (selection) => {
    const selectionString = selection[0];
    const index = selectionString.indexOf(",");
    const newTicker = selectionString.substring(0,index);
    setSelectedValue(newTicker);
    setTickerName(newTicker);
    setIsDropdownOpen(false);
  };

  /* need to parse out ticker and send it to handleSelection */
  const searchResultItems = searchResults.map((result) => (
    <li key={result} onClick={() => handleSelection(result)}> 
      {result}
    </li>
  ));

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

  // grabbing current date to set a max to the birthday input
  const currentDate = new Date();
  let [month, day, year] = currentDate.toLocaleDateString().split("/");
  // input max field must have 08 instead of 8
  month = month.length === 2 ? month : "0" + month;
  day = day.length === 2 ? day : "0" + day;
  const maxDate = year + "-" + month + "-" + day;  
  
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

  return (
    !editTrade && !bulkUpdateWithCSV ? (
      <Flex           
        flexDirection="column"
        height="100vh"
        backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
      >

       
        
        <Flex
          w='full'
          flexDirection="row"
          overflowX="auto"
          overflowY="auto"
          flex="auto"
          backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
        >
          
          {getFilterComponent()}
         
          
          <Stack
            flexDir="column"
            flex="auto"
            mb="2"
            overflowX="auto"
            overflowY="auto"
          >
          
          <Box flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" overflowX="auto" overflowY="auto">
          {authLoading ?
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
              overflowX="auto"
              overflowY="auto"
              h="full"
              w="full"
            >
            <div class='container'>
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='100px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleSelectAll(e.target.value)}>
              Select All
            </Button>
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' backgroundColor='gray.300'  color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleClearSelected(e.target.value)}>
              Clear
            </Button>
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleImportButton(e.target.value)}>
              Import
            </Button>
            {importCsvDialog}
              <AlertDialog
              motionPreset='slideInBottom'
              isOpen={importCsvDialog}
              leastDestructiveRef={cancelRef}
              onClose={e => handleCancelImportCsv(e)}
              isCentered={true}
              size='5xl'
              closeOnOverlayClick={true}
            >
              <AlertDialogOverlay>
              <AlertDialogContent>
                <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                  Import Trades from CSV
                </AlertDialogHeader>

                <AlertDialogBody>
                  Please make sure your .csv file:
                  <UnorderedList spacing={5} paddingTop={3}>
                    <ListItem>Contains <strong>only</strong> your <strong>Buy</strong> and <strong>Sell</strong> Trade History</ListItem>
                    <ListItem>All Trades must be <strong>closed out</strong> (all Buys must have a matching Sell)</ListItem>
                    <ListItem>Have the <strong>minimum required</strong> columns with matching column name (all others shown in examples are prefferred but not required):
                      <UnorderedList>
                        <ListItem>security_type</ListItem>
                        <ListItem>ticker_name</ListItem>
                        <ListItem>execution_time</ListItem>
                        <ListItem>side (Buy/Sell)</ListItem>
                        <ListItem>quantity</ListItem>
                        <ListItem>cost_basis</ListItem>
                      </UnorderedList>
                    </ListItem>
                    <ListItem>Follow this layout (may require some formatting from you!)
                    <TableContainer overflowY="auto" overflowX="auto" paddingTop={2}>
                      <Table size='sm' variant='simple'>
                        <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.800"} zIndex={2}>
                          <Tr>
                            <Th overflow='auto'>security_type</Th>
                            <Th overflow='auto'>ticker_name</Th>
                            <Th overflow='auto'>execution_time</Th>
                            <Th overflow='auto'>side</Th>
                            <Th overflow='auto'>expiry</Th>
                            <Th overflow='auto'>strike</Th>
                            <Th overflow='auto'>cost_basis</Th>
                            <Th overflow='auto'>quantity</Th>
                          </Tr>
                        </Thead>
                      </Table>
                    </TableContainer>
                    </ListItem>
                    <ListItem paddingBottom={4}>Heres an example to show a file thats ready for import:{' '} 
                      <Link href="./csv/data.csv" download="example_trade_history.csv" color='blue.500'>Download Example</Link>
                    </ListItem>
                  </UnorderedList>
                </AlertDialogBody>
                <HStack>
                <Input
                    paddingTop={1}
                    type="file"
                    id="file"
                    accept=".csv" 
                    maxWidth="400px"
                    ml={3}
                    onChange={handleFileInputChange}/>
                {tradeLoading ? <Text paddingLeft={3} color='red.500'>Loading your Trades...</Text> : ( <Text></Text>) }
                </HStack>
                <AlertDialogFooter paddingTop={10}>
                  <Button ref={cancelRef} minWidth='150px' onClick={e => handleCancelImportCsv(e)}>
                    Cancel
                  </Button>
                  {tradeLoading ?
                    <Button colorScheme='blue' minWidth='150px' ml={3}>
                      <Center>
                        <Spinner
                          thickness='2px'
                          speed='0.65s'
                          emptyColor='gray.200'
                          color='grey.500'
                          size='sm'
                        />
                      </Center>
                    </Button>
                  :
                    <Button colorScheme='blue' minWidth='150px' isDisabled={!selectedFile} onClick={e => handleConfirmImportCsv(e)} ml={3}>
                      Submit
                    </Button>
                  } 
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            </AlertDialog>
            {tradeLoading && exportLoading?
              <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' backgroundColor='gray.300'>
                <Center>
                  <Spinner
                    thickness='2px'
                    speed='0.65s'
                    emptyColor='gray.200'
                    color='grey.500'
                    size='sm'
                  />
                </Center>
              </Button>
            :
              <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleExport(e.target.value)}>
                Export
              </Button>
            }
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='100px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} onClick={(e) => handleLogTrade(e.target.value)}>
              + Add Trade
            </Button>
            {tradeLoading && !deletealertdialog && !importCsvDialog && !exportLoading && editLoading?
              <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' colorScheme='blue'>
                <Center>
                  <Spinner
                    thickness='2px'
                    speed='0.65s'
                    emptyColor='gray.200'
                    color='grey.500'
                    size='sm'
                  />
                </Center>
              </Button>
            :
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' colorScheme='blue' isDisabled={selectedRow.length === 0} onClick={e => handleGotoEdit(e)}>
              Edit
            </Button>
            }
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' colorScheme='red' isDisabled={selectedRow.length === 0} onClick={e => handleDeleteButton(e)}>
              Delete
            </Button>
            </div>
            <HStack justifyContent='end' paddingEnd='4'>
              <VscTriangleLeft isDisabled={!backPageEnable} class='pagearrows' onClick={e => handleBackPage(e)}>

              </VscTriangleLeft>
              <VscTriangleRight isDisabled={!nextPageEnable} class='pagearrows' onClick={e => handleNextPage(e)}>

              </VscTriangleRight>
              <Text class='pagenumbers'>
                {pageStartOffset}-{pageEndOffset} of {totalCount}
              </Text>
              <Divider orientation="vertical" colorScheme="gray"/>
              <Text class='numresults'>
                No. of Rows:
              </Text>
              <Select maxW={75} variant='filled' size="sm" defaultValue='100' value={num_results} onChange={(e) => handleChangeNumResults(e)}>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
                <option value="250">250</option>
                <option value="500">500</option> 
              </Select>
            </HStack>
            {hasTrades ? (
            <TableContainer overflowY="auto" overflowX="auto" rounded="lg">
              <Table size='sm' variant='simple' colorScheme='gray' borderColor={colorMode === 'light' ? "gray.100" : "gray.800"}>
                <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"} zIndex={2}>
                  <Tr>
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('trade_type')}*/>
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
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('security_type')}*/>
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
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('ticker_name')}*/>
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
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('trade_date')}*/>
                      <HStack>
                        <span>
                          Close<br></br>Date
                        </span>
                        <IconButton
                          aria-label="Sort by Close Date"
                          icon={getSortIcon('trade_date')}
                          onClick={() => requestSort('trade_date')}
                          size="xs"
                          variant="ghost"
                        />
                      </HStack>
                    </Th>
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('expiry')}*/>
                      <HStack>
                        <span>
                          Expiry
                        </span>
                        <IconButton
                          aria-label="Sort by Expiry Date"
                          icon={getSortIcon('expiry')}
                          onClick={() => requestSort('expiry')}
                          size="xs"
                          variant="ghost"
                        />
                      </HStack>
                    </Th>
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('strike')}*/>
                      <HStack>
                        <span>
                          Strike
                        </span>
                        <IconButton
                          aria-label="Sort by Strike Price"
                          icon={getSortIcon('strike')}
                          onClick={() => requestSort('strike')}
                          size="xs"
                          variant="ghost"
                        />
                      </HStack>
                    </Th>
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('buy_value')}*/>
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
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('units')}*/>
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
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('rr')}*/>
                      <HStack>
                        <span>
                          R/R
                        </span>
                        <IconButton
                          aria-label="Sort by r/r"
                          icon={getSortIcon('rr')}
                          onClick={() => requestSort('rr')}
                          size="xs"
                          variant="ghost"
                        />
                      </HStack>
                    </Th>
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('pnl')}*/>
                      <HStack>
                        <span>
                          PNL
                        </span>
                        <IconButton
                          aria-label="Sort by pnl"
                          icon={getSortIcon('pnl')}
                          onClick={() => requestSort('pnl')}
                          size="xs"
                          variant="ghost"
                        />
                      </HStack>
                    </Th>
                    <Th resize='horizontal' overflow='auto' /*onClick={() => requestSort('percent_wl')}*/>
                      <HStack>
                        <span>
                          % W/L
                        </span>
                        <IconButton
                          aria-label="Sort by % W/L"
                          icon={getSortIcon('percent_wl')}
                          onClick={() => requestSort('percent_wl')}
                          size="xs"
                          variant="ghost"
                        />
                      </HStack>
                    </Th>
                    <Th resize='horizontal' overflow='hidden' textOverflow='ellipsis'>
                      Comments
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
                          <Td>{trade.trade_date}</Td>
                          <Td>{trade.expiry}</Td>
                          <Td isNumeric>{trade.strike}</Td>
                          <Td isNumeric>{trade.buy_value}</Td>
                          <Td isNumeric>{trade.units}</Td>
                          <Td>{trade.rr}</Td>
                          <Td isNumeric>{trade.pnl}</Td>
                          <Td isNumeric>{trade.percent_wl}</Td>
                          <Td whiteSpace="normal" overflow='hidden'>{trade.comments}</Td>
                        </Tr>
                      ))}
                    </Tbody>
              </Table>
            </TableContainer>
            ) : (
            <TableContainer overflowY="auto" overflowX="auto" rounded="lg">
              <Table size='sm' variant='simple' colorScheme='gray' borderWidth="1px" borderColor={colorMode === 'light' ? "gray.100" : "gray.800"}>
                <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"} zIndex={2}>
                  <Tr>
                    <Th resize='horizontal' overflow='auto'>Trade Type</Th>
                    <Th resize='horizontal' overflow='auto'>Security Type</Th>
                    <Th resize='horizontal' overflow='auto'>Ticker</Th>
                    <Th resize='horizontal' overflow='auto'>Close Date</Th>
                    <Th resize='horizontal' overflow='auto'>Expiry</Th>
                    <Th resize='horizontal' overflow='auto'>Strike</Th>
                    <Th resize='horizontal' overflow='auto'>Avg Price</Th>
                    <Th resize='horizontal' overflow='auto'># of Units</Th>
                    <Th resize='horizontal' overflow='auto'>R/R</Th>
                    <Th resize='horizontal' overflow='auto'>PNL</Th>
                    <Th resize='horizontal' overflow='auto'>% W/L</Th>
                    <Th resize='horizontal' overflow='auto'>Comments</Th>
                  </Tr>
                </Thead>
              </Table>
            </TableContainer>
            )}
            {deletealertdialog} ? (
              <AlertDialog
              motionPreset='slideInBottom'
              isOpen={isOpen}
              leastDestructiveRef={cancelRef}
              onClose={e => handleCancelDelete(e)}
              isCentered={true}
              closeOnOverlayClick={false}
            >
            {tradeLoading && deletealertdialog?
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
                  Delete Trade
                </AlertDialogHeader>

                <AlertDialogBody>
                  Are you sure? You can't undo this action afterwards.
                </AlertDialogBody>

                <AlertDialogFooter>
                  <Button ref={cancelRef} onClick={e => handleCancelDelete(e)}>
                    Cancel
                  </Button>
                  <Button colorScheme='red' onClick={e => handleConfirmDelete(e)} ml={3}>
                    Delete
                  </Button>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
            ) : (

            )
            </Stack>
          }
          </Box>
          </Stack>
        </Flex>
      </Flex>
    ) : (
      <Flex
        flexDirection="column"
        width="100wh"
        height="100vh"
        backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
        justifyContent="center"
        alignItems="center"
        overflow="scroll"
      >
        <Stack
          class='profilestack'
        >
          {!bulkUpdateWithCSV ? (
            getEditComponent()
          ) : (
            getBulkUpdateCSVComponent()
          )}
        </Stack>
      </Flex>
    ) 
  )
}
