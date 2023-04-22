import React, { useEffect, useState } from "react";
import { getPnlByYear, getTrades, reportBug } from '../store/auth'
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
  const [page, setPage] = useState("");
  const [summary, setSummary] = useState("");
  const [description, setDescription] = useState("");
  const isBugReported = ((info && Object.keys(info).length === 1 && info.result && info.result === "Bug Ticket Created Successfully") ? (true):(false));

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();

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
        variant: 'top-accent',
        status: 'success',
        duration: 3000,
        isClosable: true
      });
    }
    setToastMessage(undefined);
  }, [toastMessage, toast]);

  const handleHome = async (e, user_id) => {
    navigate("/");
    await dispatch(getTrades({ user_id }));
  }

  const handlePnlCalendar = async (e, user_id) => {
    navigate("/PnlCalendar");
    await dispatch(getPnlByYear({ user_id, year }));
  }

  const handleTrades = async (e, user_id) => {
    navigate("/summary");
    await dispatch(getTrades({ user_id }));
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
        <Divider orientation="vertical" borderColor="grey.400"/>
      );
      content.push(
        <Heading paddingLeft={3} size='md' color="white" class='pagename'>
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
    <Flex justify="space-between" backgroundColor="teal.600">
      {((user && Object.keys(user).length > 2) && !(trade && Object.keys(trade).length > 2)) ? (
        <HStack >
        <Heading className='my-trading-tracker' m={2} size='lg' color="white" _hover={{ color: "gray.300" }} onClick={(e) => handleHome(e.target.value, user.user_id)}>
          My&#8203;Trading&#8203;Tracker
          <Icon as={RiStockFill}></Icon>
        </Heading>
        {displayPageName()}
        </HStack>
      ) : (
        <Heading m={2} size='lg' color="white">
          My&#8203;Trading&#8203;Tracker
          <Icon as={RiStockFill}></Icon>
        </Heading>
      )}
      {((user && Object.keys(user).length > 2) && !(trade && Object.keys(trade).length > 2)) ? (
        <><Spacer /><Center >
          <span>
          <ButtonGroup gap='2' padding={4} flexWrap='wrap'>
            <Button size="sm" backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handleHome(e.target.value, user.user_id)}>
              Home
            </Button>
            <Button size="sm" backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handleTrades(e.target.value, user.user_id)}>
              Trades
            </Button>
            <Button size="sm" backgroundColor="white" border='1px' borderColor='black' onClick={(e) => handlePnlCalendar(e.target.value, user.user_id)}>
              Pnl Calendar
            </Button>
            <Button size="sm" backgroundColor="#FFC257" border='1px' borderColor='black' onClick={(e) => handleReportBug(e.target.value)}>
              Report A Bug
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
                  Report Bug
                </AlertDialogHeader>

                <AlertDialogBody>
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
                    <Select id="optionsSelection" placeholder='Which Page has a Bug?' onChange={(e) => setPage(e.target.value)}>
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
                  <Button colorScheme='teal' onClick={e => handleConfirmReportBug(e)} ml={3}>
                    Submit Bug Report
                  </Button>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
        </ButtonGroup>
        </span>
        <Divider orientation="vertical" borderColor="grey.400"/>
        <span>
        <HStack>
        <Text paddingStart={4} as='kbd' className="username">
          {user.first_name}
        </Text>
        <Link as={RouterLink} to="/profile">
          <Avatar border='1px' borderColor='black' size="sm" m={2} />
        </Link>
        </HStack>
        </span>
        </Center>
        </>
      ) : null}
    </Flex>
  );
}
