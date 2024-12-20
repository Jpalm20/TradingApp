import React, { useEffect, useState } from "react";
import { getPnlByYear, getTrades, getTradesPage, reportBug, getTradesStats, getPreferences, getProfilePicture, getAccountValues, getJournalEntries, getLeaderboard } from '../store/auth'
import '../styles/navbar.css';
import moment from 'moment'; 
import 'moment-timezone';
import { 
  Flex, 
  Heading, 
  Avatar, 
  Link,
  Text,
  Center,
  Spinner,
  ButtonGroup,
  Toast,
  Input,
  InputGroup,
  useToast,
  Select,
  useColorMode,
  Image,
  Switch,
  Textarea,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  AlertDialogCloseButton,
  useDisclosure,
  FormControl,
  FormHelperText,
  Divider,
  Button,
  Spacer, 
  Icon,
  HStack} from "@chakra-ui/react";
import { Link as RouterLink, useNavigate, useLocation, parsePath} from "react-router-dom";
import { RiStockFill } from "react-icons/ri";
import { BsSun, BsMoon, BsWindowSidebar } from "react-icons/bs";
import { IoIosInformationCircleOutline } from "react-icons/io";
import { SiSwagger } from "react-icons/si";
import { useSelector, useDispatch } from "react-redux";
import logo from '../logo/mttlogo512.png';

const API_URL = process.env.REACT_APP_API_URL;
const SWAGGER_URL = API_URL+'apidocs/';
const APP_VERSION = "1.1.1";

const PAGE_NAME = [
  {page:"/home", text: "Home"}, 
  {page:"/PnlCalendar", text: "PnL Calendar"},
  {page:"/login", text: "None"},
  {page:"/signup", text: "None"},
  {page:"/logTrade", text: "None"},
  {page:"/profile", text: "User Profile"},
  {page:"/summary", text: "Trade Summary"},
  {page:"/journal", text: "Journal"},
  {page:"/leaderboard", text: "Leaderboard"},
]


export default function Navbar({ user }) {
  const location = useLocation();
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trade } = useSelector((state) => state.trade);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const { success } = useSelector((state) => state.auth);
  const today = new Date();
  const year = today.getFullYear();
  const authLoading = useSelector((state) => state.auth.loading);
  const [reportBugFlag, setReportBugFlag] = useState(false);
  const [infoPopup, setInfoPopup] = useState(false);
  const [requestType, setRequestType] = useState("");
  const [page, setPage] = useState("");
  const [summary, setSummary] = useState("");
  const [description, setDescription] = useState("");
  const isBugReported = ((info && Object.keys(info).length === 1 && info.result && info.result === "Feedback Submitted Successfully") ? (true):(false));
  const { profilepic } = useSelector((state) => state.auth); 
  const hasProfilePicture = ((profilepic && Object.keys(profilepic).length > 0) ? (true):(false)); 

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();

  const { colorMode, toggleColorMode } = useColorMode();

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  useEffect(() => {
    displayPageName();
  }, [PAGE_NAME]); 

  const evaluateSuccess = () => {
    if(success === true && isBugReported){
      setReportBugFlag(false);
      clearBugForm();
      onClose();
      setToastMessage(info.result);
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

  const toggleInfoButton = (e) => {
    setInfoPopup(true);
  }

  const handleCancelInfoPopup = (e) => {
    setInfoPopup(false);
  };

  const handleGoToSwagger = (e) => {
    window.location.href = SWAGGER_URL; // Replace with your actual Swagger URL
    //window.open(SWAGGER_URL, '_blank');
  };

  const handleHome = async (e) => {
    navigate("/");
    await dispatch(getTradesStats());
    await dispatch(getPreferences());
    let filters = {};
    filters.date = returnInTZ(today.toISOString());
    await dispatch(getAccountValues({ filters }));
    filters = {};
    filters.page = 1;
    filters.numrows = 5;
    filters.trade_date = 'NULL';
    await dispatch(getTradesPage({ filters }));
    handleDeleteLocal();
  }

  const handlePnlCalendar = async (e) => {
    navigate("/PnlCalendar");
    await dispatch(getPnlByYear({ year }));
    handleDeleteLocal();
  }

  const handleJournal = async (e) => {
    navigate("/journal");
    const date = returnInTZ(today.toISOString());
    await dispatch(getJournalEntries({ date })); 
    handleDeleteLocal();
  }

  const handleLeaderboard = async (e) => {
    navigate("/leaderboard");
    const encodedTimeFilter = encodeURIComponent("All Time");
    const encodedValueFilter = encodeURIComponent("Total PNL");
    const filters = {};
    filters.time_filter = encodedTimeFilter;
    filters.value_filter = encodedValueFilter;
    await dispatch(getLeaderboard({ filters }));
    handleDeleteLocal();
  }

  const handleProfile = async (e) => {
    navigate("/profile");
    await dispatch(getPreferences()); 
    //await dispatch(getProfilePicture());
    handleDeleteLocal();
  }

  const handleTrades = async (e) => {
    navigate("/summary");
    const filters = {};
    filters.page = 1;
    filters.numrows = 100;
    await dispatch(getTradesPage({ filters }));
    handleDeleteLocal();
  }

  const handleReportBug = (e) => {
    setReportBugFlag(true);
    onOpen();
  }

  const handleDeleteLocal = () => {
    window.localStorage.removeItem('userInfo');
    window.localStorage.removeItem('journalInfo');
    window.localStorage.removeItem('tradeInfo');
    window.localStorage.removeItem('feedbackInfo');
    window.localStorage.removeItem('updateTradeInfo');
    window.localStorage.removeItem('updateBulkTradeInfo');
    window.localStorage.removeItem('updateUserInfo');
    window.localStorage.removeItem('HomeFilters');
    window.localStorage.removeItem('CalendarFilters');
    window.localStorage.removeItem('SummaryFilters');
    window.localStorage.removeItem('LeaderboardFilters');
  } 

  
  const displayPageName = () =>{
    let content = [];
    const pageText = PAGE_NAME.find(el => el.page === location.pathname)?.text
    if (pageText !== "None"){
      content.push(
        <Divider orientation="vertical" colorScheme="gray"/>
      );
      content.push(
        <Heading class={colorMode === 'light' ? 'pagename' : 'pagenamedark'}>
          {pageText}
        </Heading>
      );
    }else{

    }
    return content;
  }

  useEffect(() => {
    const savedFeedbackInfo = window.localStorage.getItem('feedbackInfo');
    if (savedFeedbackInfo) {
      const feedbackInfo = JSON.parse(savedFeedbackInfo);
      setRequestType(feedbackInfo.requestType || "");
      setPage(feedbackInfo.page || "");
      setDescription(feedbackInfo.description || "");
      setSummary(feedbackInfo.summary || "");
    }
  }, []); // Empty dependency array means this runs once on mount

  const handleConfirmReportBug = async (e) => {
    e.preventDefault();
    const feedbackInfo = {
      requestType,
      summary,
      description,
      page 
    };
    await dispatch(
      reportBug({ 
        requestType,
        summary,
        description,
        page 
      })
    );
    window.localStorage.setItem('feedbackInfo', JSON.stringify(feedbackInfo));
  };

  const handleCancelReportBug = (e) => {
    setReportBugFlag(false);
    clearBugForm();
    onClose();
  };

  const handleClearReportBug = (e) => {
    clearBugForm();
  };

  function clearBugForm() {
    setRequestType("");
    setPage("");
    setDescription("");
    setSummary("");
    window.localStorage.removeItem('feedbackInfo');
  }

  const handleGotoLogin = (e) => {
    navigate("/login");
  };

  const handleGotoSignup = (e) => {
    navigate("/signup");
  };
  
  return (
    <Flex justify="space-between" bg={colorMode === 'light' ? "blue.500" : "blue.200"} >
      {((user && Object.keys(user).length > 2) && !(trade && Object.keys(trade).length > 2)) ? (
        <HStack >
        <Image
          class='logo'
          src={logo}
          alt='Error'
          onClick={(e) => handleHome(e.target.value)}
        />
        <Heading class={colorMode === 'light' ? 'my-trading-tracker' : 'my-trading-trackerdark'} onClick={(e) => handleHome(e.target.value)}>
          My&#8203;Trading&#8203;Tracker
          <Icon as={RiStockFill}></Icon>
        </Heading>
        {displayPageName()}
        </HStack>
      ) : (
        <HStack >
        <Image
          class='logo-alone'
          src={logo}
          alt='Error'
        />
        <Heading class={colorMode === 'light' ? 'my-trading-tracker-alone' : 'my-trading-tracker-alonedark'}>
          My&#8203;Trading&#8203;Tracker
          <Icon as={RiStockFill}></Icon>
        </Heading>
        </HStack>
      )}
      {((user && Object.keys(user).length > 2) && !(trade && Object.keys(trade).length > 2)) ? (
        <><Spacer /><Center >
          <span>
          <ButtonGroup gap='2' padding={4} flexWrap='wrap'>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleHome(e.target.value)}>
              Home
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleTrades(e.target.value)}>
              Trades
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleLeaderboard(e.target.value)}>
              Leaderboard
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handlePnlCalendar(e.target.value)}>
              Calendar
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleJournal(e.target.value)}>
              Journal
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleReportBug(e.target.value)}>
              Feedback
            </Button>
            <button className={colorMode === 'light' ? 'color-mode-comp' : 'color-mode-comp-dark'} onClick={toggleColorMode}>
              <Icon as={colorMode === 'light' ? BsSun : BsMoon}></Icon>
            </button>
            <button className={colorMode === 'light' ? 'color-mode-comp' : 'color-mode-comp-dark'} onClick={toggleInfoButton}>
              <Icon as={IoIosInformationCircleOutline}></Icon>
            </button>
            {reportBugFlag}
            <AlertDialog
              motionPreset='slideInBottom'
              isOpen={reportBugFlag}
              leastDestructiveRef={cancelRef}
              onClose={e => handleCancelReportBug(e)}
              isCentered={true}
              closeOnOverlayClick={false}
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
                  <Flex justifyContent="space-between" alignItems="center" width="100%">
                    <Text>Provide Feedback</Text>
                    <Button size='sm' colorScheme='blue' onClick={e => handleClearReportBug(e)}>
                      Clear
                    </Button>
                  </Flex>
                </AlertDialogHeader>
                
                <AlertDialogBody>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Feedback Type *
                    </FormHelperText>
                    <Select id="optionsSelection" value={requestType} placeholder='Bug Report or Feature Request?' onChange={(e) => setRequestType(e.target.value)}>
                    <option>Bug Report</option>
                    <option>Feature Request</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Summary *
                    </FormHelperText>
                    <InputGroup>
                      <Input
                        type="name"
                        value={summary}
                        onChange={(e) => setSummary(e.target.value)}
                      />
                    </InputGroup>
                  </FormControl>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Page *
                    </FormHelperText>
                    <Select id="optionsSelection" value={page} placeholder='Which Page is affected?' onChange={(e) => setPage(e.target.value)}>
                    <option>Login</option>
                    <option>Signup</option>
                    <option>Home</option>
                    <option>Trade Summary Table</option>
                    <option>PnL Calendar</option>
                    <option>Journal</option>
                    <option>User Profile</option>
                    <option>Other</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Description *
                    </FormHelperText>
                    <Textarea value={description} placeholder='Describe the bug you are experiencing...' onChange={(e) => setDescription(e.target.value)}/>
                  </FormControl>
                </AlertDialogBody>

                <AlertDialogFooter>
                  <Button ref={cancelRef} onClick={e => handleCancelReportBug(e)}>
                    Cancel
                  </Button>
                  <Button colorScheme='blue' onClick={e => handleConfirmReportBug(e)} ml={3}>
                    Submit
                  </Button>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
            {infoPopup}
              <AlertDialog
              motionPreset='slideInBottom'
              isOpen={infoPopup}
              leastDestructiveRef={cancelRef}
              onClose={e => handleCancelInfoPopup(e)}
              isCentered={true}
              closeOnOverlayClick={true}
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
                  <Flex alignItems="center" width="100%">
                    <IoIosInformationCircleOutline/>
                    <Text paddingLeft={1}>Information</Text>
                  </Flex>
                </AlertDialogHeader>
                <AlertDialogCloseButton />
                <AlertDialogBody>
                  <Center>
                  <HStack>
                  <button className={colorMode === 'light' ? 'color-mode-comp-dark' : 'color-mode-comp'} onClick={e => handleGoToSwagger(e)}>
                    <Icon as={SiSwagger}></Icon>
                  </button>
                  <Text>
                    API Documentation
                  </Text>
                  </HStack>
                  </Center>
                </AlertDialogBody>

                <AlertDialogFooter>
                  <Text as='i'>
                    v{APP_VERSION}
                  </Text>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
        </ButtonGroup>
        </span>
        <Divider orientation="vertical" colorScheme="gray"/>
        <span>
        <HStack paddingRight={2}>
        {user.first_name !== "" ? (
        <Text class={colorMode === 'light' ? "username" : "usernamedark"}>
          {user.first_name}
        </Text>
        ) : (
          null
        )}
        <Avatar  
          size="sm" 
          src={hasProfilePicture ? profilepic.profile_picture_url : null}
          m={2} 
          onClick={(e) => handleProfile(e.target.value)}
        />
        </HStack>
        </span>
        </Center>
        </>
      ) : (
        <ButtonGroup gap='2' padding={4} flexWrap='wrap'>
          {location.pathname === "/" ? (
            <>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleGotoLogin(e.target.value)}>
              Sign In
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleGotoSignup(e.target.value)}>
              Sign Up
            </Button>
            <button className={colorMode === 'light' ? 'color-mode-comp' : 'color-mode-comp-dark'} onClick={toggleColorMode}>
              <Icon as={colorMode === 'light' ? BsSun : BsMoon}></Icon>
            </button>
            </>
          ) : (
            <button className={colorMode === 'light' ? 'color-mode-comp' : 'color-mode-comp-dark'} onClick={toggleColorMode}>
              <Icon as={colorMode === 'light' ? BsSun : BsMoon}></Icon>
            </button>
          )}
        </ButtonGroup>
      )
      }
    </Flex>
  );
}
