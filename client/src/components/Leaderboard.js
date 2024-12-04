import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from "react-redux";
import { Editor } from 'ckeditor5-custom-build-light/build/ckeditor';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import { getLeaderboard} from '../store/auth'
import { Link as RouterLink, useNavigate, useLocation} from "react-router-dom";
import '../styles/summary.css';
import '../styles/logtrade.css';
import '../styles/filter.css';
import '../styles/leaderboard.css';
import moment from 'moment'; 
import 'moment-timezone';
import axios from "axios";
import { VscTriangleLeft, VscTriangleRight } from "react-icons/vsc";
import {
  Flex,
  Alert,
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
  VStack
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import tradeReducer, { update, getTrade, reset, deleteTrade, searchTicker, importCsv, exportCsv } from '../store/trade';


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

export default function Leaderboard({ user }) {
  const btnRef = React.useRef()
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const query = useQuery();
  const { success } = useSelector((state) => state.auth);
  const { leaderboard } = useSelector((state) => state.auth);
  const hasLeaderboard = ((leaderboard && leaderboard.leaderboard && Object.keys(leaderboard.leaderboard).length > 0) ? (true):(false));
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const { preferences } = useSelector((state) => state.auth); 
  const hasPreferences = ((preferences && Object.keys(preferences).length > 0) ? (true):(false)); 
  const user_id = user.user_id;
  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();
  const authLoading = useSelector((state) => state.auth.loading);
  const { colorMode, toggleColorMode } = useColorMode();

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }

  const today = returnInTZ(new Date().toISOString());

  const [leaderboardTimeFilter, setLeaderboardTimeFilter] = useState("All Time");
  const [leaderboardStatFilter, setLeaderboardStatFilter] = useState("Total PNL");
  
  const [profileStatusPopUpEnable, setProfileStatusPopUpEnable] = useState(true);
  const profileToastTriggered = React.useRef(false);

  useEffect(() => {
    if (profileStatusPopUpEnable) {
      profileStatusToast();
      setProfileStatusPopUpEnable(false); // Update state
    }
  }, [profileStatusPopUpEnable]);  

  useEffect(() => {
    handleLeaderboardFilterChange();
  }, [leaderboardTimeFilter,leaderboardStatFilter]); 
  
  useEffect(() => {
    const savedLeaderboardFilters = window.localStorage.getItem('LeaderboardFilters');
    if (savedLeaderboardFilters) {
      const LeaderboardFilters = JSON.parse(savedLeaderboardFilters);
      setLeaderboardStatFilter(LeaderboardFilters.value_filter || "Total PNL");
      setLeaderboardTimeFilter(LeaderboardFilters.time_filter || "All Time");
    }
  }, []); 

  /*
  useEffect(() => {
    evaluateSuccess();
  }, [success]); 
  */

  /*
  const evaluateSuccess = async () => {
    const date = selected_date;
    if(success === true && info && info.result && info.result === "Journal Entry Successfully Deleted"){
      await dispatch(getJournalEntries({ date }));
      setToastMessage(info.result);
    }else if (success === true && info && info.result && info.result === "Journal Entry Successfully Saved"){
      await dispatch(getJournalEntries({ date }));
      setToastMessage(info.result);
    }
  }
  */


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
        duration: 10000,
        isClosable: true
      });
    }
    setToastErrorMessage(undefined);
  }, [toastErrorMessage, toast]);

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

  const handleLeaderboardFilterChange = async () => {
    const encodedTimeFilter = encodeURIComponent(leaderboardTimeFilter);
    const encodedValueFilter = encodeURIComponent(leaderboardStatFilter);
    const filters = {};
    filters.time_filter = encodedTimeFilter;
    filters.value_filter = encodedValueFilter;
    await dispatch(getLeaderboard({ filters }));
    handleFilterChange(filtersToQueryString(filters));
    const saveFilters = {};
    saveFilters.time_filter = leaderboardTimeFilter;
    saveFilters.value_filter = leaderboardStatFilter;
    window.localStorage.setItem('LeaderboardFilters', JSON.stringify(saveFilters));
  }

  const profileStatusToast = () => {
    if (profileToastTriggered.current) return; // Prevent repeated execution
  
    const message = `Your Profile is ${
      hasPreferences && preferences["public_profile_optin"] === 1 ? "Public" : "Private"
    }`;
  
    toast({
      title: message,
      description: "You can change your leaderboard visibility in user settings",
      variant: "solid",
      status: "info",
      duration: null,
      isClosable: true,
      position: "top",
    });
  
    profileToastTriggered.current = true; // Mark as triggered
  };

  
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
          overflowX="auto"
          overflowY="auto"
          flex="auto"
          backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
        >
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
              p="3rem"
              backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
              boxShadow="md"
              overflowX="auto"
              overflowY="auto"
              h="full"
              w="full"
            >
              <div 
                className={colorMode === 'light' ? 'paper-box-small' : 'paper-box-small-dark'}
              >
                {["Total PNL", "Avg PNL", "Win %", "Largest Win", "Avg Win", "Avg Loss"].map((filter) => (
                  <Button
                    key={filter}
                    size="sm"
                    width='100px'
                    backgroundColor={leaderboardStatFilter === filter ? (colorMode === 'light' ? "blue.500" : "blue.200") : 'gray.300'}
                    color={leaderboardStatFilter === filter ? (colorMode === 'light' ? "white" : "gray.800") : (colorMode === 'light' ? "none" : "gray.800")}
                    onClick={leaderboardStatFilter === filter ? null : () => setLeaderboardStatFilter(filter)}
                  >
                    {filter}
                  </Button>
                ))}
              </div>
              <div 
                class={colorMode === 'light' ? 'paper-box-small' : 'paper-box-small-dark'}
              >
                {["All Time", "YTD", "Quarter", "Month", "Week", "Today"].map((filter) => (
                  <Button
                    key={filter}
                    size="sm"
                    width='100px'
                    backgroundColor={leaderboardTimeFilter === filter ? (colorMode === 'light' ? "blue.500" : "blue.200") : 'gray.300'}
                    color={leaderboardTimeFilter === filter ? (colorMode === 'light' ? "white" : "gray.800") : (colorMode === 'light' ? "none" : "gray.800")}
                    onClick={leaderboardTimeFilter === filter ? null : () => setLeaderboardTimeFilter(filter)}
                  >
                    {filter}
                  </Button>
                ))}
              </div>
              {hasLeaderboard ? 
                <div class={colorMode === 'light' ? 'paper-board-box' : 'paper-board-box-dark'}>
                  <TableContainer overflowY="auto" maxHeight="300px" rounded="lg">
                    <Table size='sm' variant='striped' colorScheme={colorMode === 'light' ? 'white' : "gray.700"}>
                      <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"}>
                        <Tr>
                          <Th resize='horizontal' overflow='auto' width='25px'>Position</Th>
                          <Th resize='horizontal' overflow='auto' width='150px' textAlign="center">User</Th>
                          <Th resize='horizontal' overflow='auto' textAlign="center">Value ({leaderboardStatFilter})</Th>
                        </Tr>
                      </Thead>
                          <Tbody>
                            {leaderboard.leaderboard.map((leaderboard, index) => (
                              <Tr>
                                <Td>{index+1}</Td>
                                <Td>{leaderboard.display_name}</Td>
                                <Td isNumeric>{leaderboard.leaderboard_value}</Td>
                              </Tr>
                            ))}
                          </Tbody>
                    </Table>
                  </TableContainer>
                </div>
              : 
                <div class={colorMode === 'light' ? 'paper-board-box' : 'paper-board-box-dark'}>
                  <TableContainer overflowY="auto" maxHeight="300px" rounded="lg">
                    <Table size='sm' variant='striped' colorScheme={colorMode === 'light' ? 'white' : "gray.700"}>
                      <Thead position="sticky" top={0} bgColor={colorMode === 'light' ? "lightgrey" : "gray.700"}>
                        <Tr>
                          <Th resize='horizontal' overflow='auto' width='25px'>Position</Th>
                          <Th resize='horizontal' overflow='auto' width='150px' textAlign="center">User</Th>
                          <Th resize='horizontal' overflow='auto' textAlign="center">Value ({leaderboardStatFilter})</Th>
                        </Tr>
                      </Thead>
                    </Table>
                  </TableContainer>
                </div>
              }
            ) : (

            )
            </Stack>
          }
          </Box>
          </Stack>
        </Flex>
      </Flex>
  )
}