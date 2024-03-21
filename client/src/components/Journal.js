import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from "react-redux";
import { Editor } from 'ckeditor5-custom-build-light/build/ckeditor';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import { getJournalEntries, clearJournalEntry, postJournalEntry} from '../store/auth'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import '../styles/summary.css';
import '../styles/logtrade.css';
import '../styles/filter.css';
import '../styles/journal.css';
import moment from 'moment'; 
import 'moment-timezone';
import axios from "axios";
import { VscTriangleLeft, VscTriangleRight } from "react-icons/vsc";
import {
  Flex,
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

export default function Journal({ user }) {
  const btnRef = React.useRef()
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const dispatch = useDispatch();
  const { success } = useSelector((state) => state.auth);
  const { journalentries } = useSelector((state) => state.auth);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  //const hasEntries = ((journalentries && journalentries.entries && Object.keys(journalentries.entries).length > 0) ? (true):(false));
  const hasEntries = ((journalentries && journalentries.entries) ? (true):(false));


  const user_id = user.user_id;

  const [backPageEnable, setBackPageEnable] = useState(false);
  const [nextPageEnable, setNextPageEnable] = useState(false);


  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();
  const [deletealertdialog, setDeleteAlertDialog] = useState(false);

  const authLoading = useSelector((state) => state.auth.loading);

  const [saveLoading, setSaveLoading] = useState(false);


  const [isEdit, setIsEdit] = useState(false);

  const { colorMode, toggleColorMode } = useColorMode();

  const [entryy, setEntry] = useState("");

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }

  const today = returnInTZ(new Date().toISOString());
  const [currentmonth, setCurrentMonth] = useState(moment(today).month());
  const [currentyear, setCurrentYear] = useState(moment(today).year());


  const [selected_date, setSelectedDate] = useState(today);

  const [backpageclick, setBackPageClick] = useState(false);
  const [nextpageclick, setNextPageClick] = useState(false);

  useEffect(() => {
    const todayDate = today;
    const savedJournalInfo = window.localStorage.getItem('journalInfo');
    if (savedJournalInfo) {
      const journalInfo = JSON.parse(savedJournalInfo);
      setEntry(journalInfo.entry || "");
      setSelectedDate(journalInfo.date || todayDate);
      // Clear the saved info after loading it
      //window.localStorage.removeItem('userInfo');
    }
  }, []); // Empty dependency array means this runs once on mount

  useEffect(() => {
    evaluateDateArrows();
  }, [selected_date]);


  useEffect(() => {
    //Check for if journal entry exists yet that matches entryy otherwise put into edit mode
    if (entryy !== ''){
      const entry = entryy;
      const date = selected_date;
      const journalInfo = {
        date,
        entry
      };
      window.localStorage.setItem('journalInfo', JSON.stringify(journalInfo));
    }
    if (hasEntries) {
      const existingentry = journalentries.entries.find(entry => entry.date === selected_date)?.entrytext || '';
      if (existingentry !== entryy && entryy !== ''){
        setIsEdit(true);
      }
    }
    
    // This should basically mean if you were previously editing and saving didnt work put back into edit and load entryy text
    // Right now it is doing some checks in the WYSIWYG editor but because journal entry object is empty for that day it is loading entryy text but not in edit mode, and when I edit it is blank
  }, [entryy,hasEntries]);
  

  const evaluateDateArrows = async () => {
    if(selected_date === today){
      setNextPageEnable(false);
    }
    else{
      setNextPageEnable(true);
    }

    if(selected_date === "1900-01-01"){
      setBackPageEnable(false);
    }else{
      setBackPageEnable(true);
    }

    const date = selected_date;
    if(moment(selected_date).date() === 1){
      if(nextpageclick === true){
        await dispatch(getJournalEntries({ date })); 
      }else if(backpageclick === true) {
      }
    }else if (moment(selected_date).add(1, 'days').date() === 1){
      if(nextpageclick === true){
      }else if(backpageclick === true) {
        await dispatch(getJournalEntries({ date }));
      }
    }
    setNextPageClick(false);
    setBackPageClick(false);

    //Need to add condition when user selects from date component
    if(moment(selected_date).month() !== currentmonth || moment(selected_date).year() !== currentyear){
      await dispatch(getJournalEntries({ date }));
      setCurrentMonth(moment(selected_date).month());
      setCurrentYear(moment(selected_date).year());
    }
  }

  const handleNextPage = () => {
    if(nextPageEnable){
      setEntry('');
      window.localStorage.removeItem('journalInfo');
      setIsEdit(false);
      setNextPageClick(true);
      setSelectedDate(moment(selected_date).add(1, 'days').format('YYYY-MM-DD'));
    }
  }

  const handleBackPage = () => {
    if(backPageEnable){
      setEntry('');
      window.localStorage.removeItem('journalInfo');
      setIsEdit(false);
      setBackPageClick(true);
      setSelectedDate(moment(selected_date).add(-1, 'days').format('YYYY-MM-DD'));
    }
  }

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 


  const evaluateSuccess = async () => {
    const date = selected_date;
    if(success === true && info && info.result && info.result === "Journal Entry Successfully Deleted"){
      setIsEdit(false);
      await dispatch(getJournalEntries({ date }));
      window.localStorage.removeItem('journalInfo');
      setToastMessage(info.result);
    }else if (success === true && info && info.result && info.result === "Journal Entry Successfully Saved"){
      setIsEdit(false);
      await dispatch(getJournalEntries({ date }));
      window.localStorage.removeItem('journalInfo');
      setToastMessage(info.result);
    }else if (success === true && info && info.result && info.result === "Journal Entry Successfully Updated"){
      setIsEdit(false);
      await dispatch(getJournalEntries({ date }));
      window.localStorage.removeItem('journalInfo');
      setToastMessage(info.result);
    }else if (success === true && info && info.result && info.result === "Journal Entry Successfully Deleted"){
      setIsEdit(false);
      await dispatch(getJournalEntries({ date }));
      window.localStorage.removeItem('journalInfo');
      setToastMessage(info.result);
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


  const handleCancel = () => {
    setEntry('');
    window.localStorage.removeItem('journalInfo');
    setIsEdit(false);
  };

  const handleSave = async () => {
    const entry = entryy
    const date = selected_date;
    const existingentry = journalentries.entries.find(entry => entry.date === selected_date)?.entrytext || '';
    if(entry === "" && existingentry !== ''){
      setSaveLoading(true);
      await dispatch(clearJournalEntry({ date }));
      setSaveLoading(false);
    }else if (entry !== ""){
      setSaveLoading(true);
      await dispatch(postJournalEntry({ date, entry }));
      setSaveLoading(false);
    }else{
      setToastErrorMessage("Please enter information before trying to Save");
    }
  };

  const handleGotoEdit = (e) => {
    e.preventDefault();
    if(!isEdit){
      setEntry(journalentries.entries.find(entry => entry.date === selected_date)?.entrytext || '');
      window.localStorage.removeItem('journalInfo');
      setIsEdit(true);
    }
  };

  const handleClearEntry = (e) => {
    e.preventDefault();
    setEntry('');
    window.localStorage.removeItem('journalInfo');
    setIsEdit(true);
  };


  const handleEntryDisplay = () => {
    let content = [];
    content.push(
      <div class={`paper-content ${colorMode === 'light' ? 'paper-content-light' : 'paper-content-dark'}`}>
        <CKEditor
          editor={Editor}
          data={hasEntries && !isEdit ? (journalentries.entries.find(entry => entry.date === selected_date)?.entrytext || entryy) : entryy}
          disabled={!isEdit}
          onChange={(event, editor) => {
            const data = editor.getData();
            setEntry(data);
          }}
        />
      </div>
    );
    return content
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
          {authLoading && !saveLoading ?
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
            {authLoading && saveLoading ?
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
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} isDisabled={!isEdit} onClick={(e) => handleSave()}>
              Save
            </Button>
            }
            <Button style={colorMode === 'light' ? { boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' } : { boxShadow: '2px 4px 4px rgba(256,256,256,0.2)' }} size="sm" marginLeft={3} marginBottom={2} width='75px' backgroundColor='gray.300' color={colorMode === 'light' ? "none" : "gray.800"} isDisabled={!isEdit} onClick={(e) => handleCancel()}>
              Cancel
            </Button>
            </div>
            <HStack justifyContent='center' paddingEnd='4'>
              <VscTriangleLeft isDisabled={!backPageEnable} class='pagearrowsjournal' onClick={handleBackPage}>

              </VscTriangleLeft>
              <div class={colorMode === 'light' ? 'paper-box' : 'paper-box-dark'}>
                <VStack >
                  <HStack class='button-container'>
                    <Button onClick={e => handleClearEntry(e)}>
                      Clear
                    </Button>
                    <Input
                      maxWidth='50%'
                      type="date"
                      max={maxDate}
                      min="1900-01-01"
                      value={selected_date}
                      onChange={(e) => {
                        setSelectedDate(e.target.value);
                        window.localStorage.removeItem('journalInfo');
                      }}
                    />
                    <Button onClick={e => handleGotoEdit(e)}>
                      Edit
                    </Button>
                  </HStack>
                  {handleEntryDisplay()}
                </VStack>
              </div>
              <VscTriangleRight isDisabled={!nextPageEnable} class='pagearrowsjournal' onClick={handleNextPage}>

              </VscTriangleRight>
            </HStack>
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