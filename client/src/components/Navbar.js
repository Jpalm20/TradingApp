import React, { useEffect, useState } from "react";
import { getPnlByYear, getTrades, getTradesPage, reportBug, getTradesStats, getPreferences, getAccountValues } from '../store/auth'
import '../styles/navbar.css';
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
  useDisclosure,
  FormControl,
  FormHelperText,
  Divider,
  Button,
  Spacer, 
  Icon,
  HStack} from "@chakra-ui/react";
import { Link as RouterLink, useNavigate, useLocation} from "react-router-dom";
import { RiStockFill } from "react-icons/ri";
import { useSelector, useDispatch } from "react-redux";
import logo from '../logo/mttlogo512.png';

const PAGE_NAME = [
  {page:"/home", text: "Home"}, 
  {page:"/PnlCalendar", text: "PnL Calendar"},
  {page:"/login", text: "None"},
  {page:"/signup", text: "None"},
  {page:"/logTrade", text: "None"},
  {page:"/profile", text: "User Profile"},
  {page:"/summary", text: "Trade Summary"},
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
  const [requestType, setRequestType] = useState("");
  const [page, setPage] = useState("");
  const [summary, setSummary] = useState("");
  const [description, setDescription] = useState("");
  const isBugReported = ((info && Object.keys(info).length === 1 && info.result && info.result === "Feedback Submitted Successfully") ? (true):(false));

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();

  const { colorMode, toggleColorMode } = useColorMode();

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  useEffect(() => {
    displayPageName();
  }, [PAGE_NAME]); 

  const evaluateSuccess = () => {
    if(success === true && isBugReported){
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

  const handleHome = async (e) => {
    navigate("/");
    await dispatch(getTradesStats());
    await dispatch(getPreferences());
    await dispatch(getAccountValues());
  }

  const handlePnlCalendar = async (e) => {
    navigate("/PnlCalendar");
    await dispatch(getPnlByYear({ year }));
  }

  const handleTrades = async (e) => {
    navigate("/summary");
    const filters = {};
    filters.page = 1;
    filters.numrows = 100;
    await dispatch(getTradesPage({ filters }));
  }

  const handleReportBug = (e) => {
    setReportBugFlag(true);
    onOpen();
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

  const handleConfirmReportBug = async (e) => {
    e.preventDefault();
    await dispatch(
      reportBug({ 
        requestType,
        summary,
        description,
        page 
      })
    );   
    setReportBugFlag(false);
    clearBugForm();
    onClose();
  };

  const handleCancelReportBug = (e) => {
    setReportBugFlag(false);
    clearBugForm();
    onClose();
  };

  function clearBugForm() {
    setPage("");
    setDescription("");
    setSummary("");
  }
  
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
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handlePnlCalendar(e.target.value)}>
              Calendar
            </Button>
            <Button size="sm" colorScheme="blackAlpha" onClick={(e) => handleReportBug(e.target.value)}>
              Provide Feedback
            </Button>
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
                  Provide Feedback
                </AlertDialogHeader>

                <AlertDialogBody>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Feedback Type *
                    </FormHelperText>
                    <Select id="optionsSelection" placeholder='Bug Report or Feature Request?' onChange={(e) => setRequestType(e.target.value)}>
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
                        onChange={(e) => setSummary(e.target.value)}
                      />
                    </InputGroup>
                  </FormControl>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Page *
                    </FormHelperText>
                    <Select id="optionsSelection" placeholder='Which Page is affected?' onChange={(e) => setPage(e.target.value)}>
                    <option>Login</option>
                    <option>Signup</option>
                    <option>Home</option>
                    <option>Trade Summary Table</option>
                    <option>PnL Calendar</option>
                    <option>User Profile</option>
                    <option>Other</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Description *
                    </FormHelperText>
                    <Textarea placeholder='Describe the bug you are experiencing...' onChange={(e) => setDescription(e.target.value)}/>
                  </FormControl>
                </AlertDialogBody>

                <AlertDialogFooter>
                  <Button ref={cancelRef} onClick={e => handleCancelReportBug(e)}>
                    Cancel
                  </Button>
                  <Button colorScheme='blue' onClick={e => handleConfirmReportBug(e)} ml={3}>
                    Submit Feedback
                  </Button>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
        </ButtonGroup>
        </span>
        <Divider orientation="vertical" colorScheme="gray"/>
        <span>
        <HStack>
        <Text class={colorMode === 'light' ? "username" : "usernamedark"}>
          {user.first_name}
        </Text>
        <Link as={RouterLink} to="/profile">
          <Avatar size="sm" m={2} />
        </Link>
        </HStack>
        </span>
        </Center>
        </>
      ) : null}
    </Flex>
  );
}
