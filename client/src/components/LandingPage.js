import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from "react-redux";
import { Link as RouterLink, useNavigate} from "react-router-dom";
import '../styles/landingpage.css';
import axios from "axios";
import Home from '../assets/Home.png'
import Calendar from '../assets/Calendar.png'
import TradeSummary from '../assets/TradeSummary.png'
import Journal from '../assets/Journal.png'
import HomeLight from '../assets/Home-Light.png'
import CalendarLight from '../assets/Calendar-Light.png'
import TradeSummaryLight from '../assets/TradeSummary-Light.png'
import JournalLight from '../assets/Journal-Light.png'
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
  Tabs, 
  TabList, 
  TabPanels, 
  Tab, 
  TabPanel,
  Center,
  UnorderedList,
  ListItem,
  Spinner,
  List,
  ListIcon,
  OrderedList,
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
  Card,
  CardBody,
  Image,
  Divider,
  CardFooter,
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
import { HiOutlineMail } from "react-icons/hi";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { BsFilePersonFill, BsCalendarEvent, BsJournal } from "react-icons/bs";
import { IoAnalyticsSharp } from "react-icons/io5";
import { FiMonitor } from "react-icons/fi";
import { RiStockFill } from "react-icons/ri";



const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function LandingPage() {
  const btnRef = React.useRef()
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { colorMode, toggleColorMode } = useColorMode();

  const words = ['tracker', 'journal', 'manager', 'application', 'tool', 'hub', 'analyzer'];
  const [wordIndex, setWordIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [text, setText] = useState('');

  useEffect(() => {
    const type = () => {
      const currentWord = words[wordIndex];
      if (isDeleting) {
        if (charIndex === 0) {
          setIsDeleting(false);
          setWordIndex((prevWordIndex) => (prevWordIndex + 1) % words.length);
        } else {
          setText(currentWord.substring(0, charIndex));
          setCharIndex((prevCharIndex) => prevCharIndex - 1);
        }
      } else {
        setText(currentWord.substring(0, charIndex));
        if (charIndex === currentWord.length) {
          setIsDeleting(true);
        } else {
          setCharIndex((prevCharIndex) => prevCharIndex + 1);
        }
      }
    };

    const typingDelay = isDeleting ? 100 : 250;
    const nextTyping = setTimeout(type, typingDelay);
    return () => clearTimeout(nextTyping); // Cleanup the timer
  }, [text, charIndex, isDeleting, wordIndex, words]);

  useEffect(() => {
    const nextWordDelay = setTimeout(() => {
      if (isDeleting) {
        setCharIndex(words[wordIndex].length);
      }
    }, 1000);
    return () => clearTimeout(nextWordDelay); // Cleanup the timer
  }, [isDeleting]);

  const [tabIndex, setTabIndex] = useState(0);

  const handleAnchorClick = (event, id, index) => {
    event.preventDefault();
    const element = document.getElementById(id);
    setTabIndex(index);
    element.scrollIntoView({ behavior: 'smooth' });
  };
     

  return (
    <Flex
        flexDirection="column"
        backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
        width="100wh"
        height="100vh"
        alignItems="center" // Add this line to center content horizontally
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
        overflowX="auto"
        overflowY="auto"
        alignItems="center" // Add this line to center content horizontally
      >
        <VStack paddingBottom={100}>
            <HStack 
                alignItems="stretch" 
                paddingTop={100} 
                paddingLeft="15%" 
                paddingRight="15%" 
                paddingBottom={70}
            >
                <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>your personal <br></br>trading {text}|</Heading>
                <Text as='samp' w='50%' class={colorMode === 'light' ? 'headertext' : 'headertextdark'}>
                    Elevate Your Trading Journey with our all-in-one tool.
                        <Center paddingTop={3} paddingBottom={3}>
                            <Icon fontSize='lg' as={RiStockFill}></Icon>
                        </Center>
                    Introducing MyTradingTracker, your comprehensive platform for seamless trading log management, insightful analysis, and interactive journaling. Streamline your trading process, enhance review mechanisms, and unlock opportunities for substantial growth and improvement.                
                </Text>
            </HStack>

            <Tabs 
                isFitted
                variant='solid-rounded' 
                colorScheme='blue' 
                defaultIndex={0} 
                index={tabIndex}
                overflowX="auto"  // Allow horizontal scrolling
            >
                <TabPanels id='tab-panels'>
                    <TabPanel 
                        display="flex"
                        alignItems="center"  // Center content vertically
                        justifyContent="center"  // Center content horizontally
                    >
                        <Box 
                            overflowX="auto"  // Allow horizontal scrolling
                            minW={{ base: "90%", md: "500px" }} 
                            maxW={{ base: "90%", md: "900px" }} 
                            rounded="lg" 
                            style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}
                        >
                            <Box
                                display="flex"
                                alignItems="center"  // Center content vertically
                                justifyContent="center"  // Center content horizontally
                                w="100%"
                                h="100%"
                                rounded="lg"
                                overflow="auto"  // Allow horizontal scrolling
                            >
                                <Stack
                                flex='auto'
                                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
                                boxShadow="md"
                                w="100%"
                                h="100%"
                                overflow='auto'
                                alignItems="center" // Add this line to center content horizontally
                                justifyContent="center" // Add this line to center content vertically
                                >
                                <Card h='100%' overflowY='auto'>
                                    <CardBody h='100%'>
                                    <Image
                                        src={colorMode === 'light' ? HomeLight : Home}
                                        alt='Home Screen'
                                        borderRadius='lg'
                                    />
                                    <Stack display='flex' alignItems='center' mt='6' spacing='3'>
                                        <Heading size='md'>Summary Page</Heading>
                                        <Text paddingTop='5px' h='175px'>
                                        This page is your home base. Enjoy an overview of your trading activity, accompanied by relavant statistics and a visual of your trading account balance. 
                                        <br></br>
                                        <br></br>
                                        This includes the ability to filter results by time or value in order extract data under certain conditions.
                                        Feel free to set and/or update your account balance from this screen as well!
                                        <br></br>
                                        </Text>
                                    </Stack>
                                    </CardBody>
                                </Card>
                                </Stack>
                            </Box>
                        </Box>
                    </TabPanel>
                    <TabPanel 
                        display="flex"
                        alignItems="center"  // Center content vertically
                        justifyContent="center"  // Center content horizontally
                    >
                        <Box 
                            overflowX="auto"  // Allow horizontal scrolling
                            minW={{ base: "90%", md: "500px" }} 
                            maxW={{ base: "90%", md: "900px" }} 
                            rounded="lg" 
                            style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}
                        >
                            <Box
                                display="flex"
                                alignItems="center"  // Center content vertically
                                justifyContent="center"  // Center content horizontally
                                w="100%"
                                h="100%"
                                rounded="lg"
                                overflow="auto"  // Allow horizontal scrolling
                            >
                                <Stack
                                flex='auto'
                                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
                                boxShadow="md"
                                w="100%"
                                h="100%"
                                overflow='auto'
                                alignItems="center" // Add this line to center content horizontally
                                justifyContent="center" // Add this line to center content vertically
                                >
                                <Card h='100%' overflowY='auto'>
                                    <CardBody h='100%' >
                                    <Image
                                        src={colorMode === 'light' ? TradeSummaryLight : TradeSummary}
                                        alt='Trade Summary Screen'
                                        borderRadius='lg'
                                    />
                                    <Stack display='flex' alignItems='center' mt='6' spacing='3' >
                                        <Heading size='md'>Trade Management</Heading>
                                        <Text paddingTop='5px' h='175px' >
                                        Here is where you will log, import, add, edit and delete trade entries from your account.
                                        <br></br>
                                        <br></br>
                                        You can think of it this way... this page is for adding your trade data (through multiple avenues) while other pages are for viewing this information in a formatted manner.
                                        This formatting is what allows you to see whats between the lines, maybe you trade specific tickers better, or maybe theres a flaw in your trading that was noticed through analysis.
                                        Getting a little off track, but the point is, without your adding data here the rest of the app is useless, so you will be spending plenty of time here!
                                        <br></br>
                                        </Text>
                                    </Stack>
                                    </CardBody>
                                </Card>
                                </Stack>
                            </Box>
                        </Box>
                    </TabPanel>
                    <TabPanel 
                        display="flex"
                        alignItems="center"  // Center content vertically
                        justifyContent="center"  // Center content horizontally
                    >
                        <Box 
                            overflowX="auto"  // Allow horizontal scrolling
                            minW={{ base: "90%", md: "500px" }} 
                            maxW={{ base: "90%", md: "900px" }} 
                            rounded="lg" 
                            style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}
                        >
                            <Box
                                display="flex"
                                alignItems="center"  // Center content vertically
                                justifyContent="center"  // Center content horizontally
                                w="100%"
                                h="100%"
                                rounded="lg"
                                overflow="auto"  // Allow horizontal scrolling
                            >
                                <Stack
                                flex='auto'
                                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
                                boxShadow="md"
                                w="100%"
                                h="100%"
                                overflow='auto'
                                alignItems="center" // Add this line to center content horizontally
                                justifyContent="center" // Add this line to center content vertically
                                >
                                <Card h='100%' overflowY='auto'>
                                    <CardBody h='100%'>
                                    <Image
                                        src={colorMode === 'light' ? CalendarLight : Calendar}
                                        alt='Pnl Calendar'
                                        borderRadius='lg'
                                    />
                                    <Stack display='flex' alignItems='center' mt='6' spacing='3'>
                                        <Heading size='md'>Calendar View</Heading>
                                        <Text paddingTop='5px' h='175px'>
                                        It is common for traders to look at their trades and daily profit and loss in relation to time, specifically calendars.
                                        This is a way for you to visualize your trading on a daily, weekly and monthly basis and see how your overall trading results vary month by month.
                                        Being able to quantify your progress when things get tough is a tool every trader needs.
                                        <br></br>
                                        <br></br>
                                        *Heres a hint: Click on top of the calendar boxes and youll be able to see all trades closed on that calendar day, as well as some important information about each trade.
                                        <br></br>
                                        </Text>
                                    </Stack>
                                    </CardBody>
                                </Card>
                                </Stack>
                            </Box>
                        </Box>
                    </TabPanel>
                    <TabPanel 
                        display="flex"
                        alignItems="center"  // Center content vertically
                        justifyContent="center"  // Center content horizontally
                    >
                        <Box 
                            overflowX="auto"  // Allow horizontal scrolling
                            minW={{ base: "90%", md: "500px" }} 
                            maxW={{ base: "90%", md: "900px" }} 
                            rounded="lg" 
                            style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}
                        >
                            <Box
                                display="flex"
                                alignItems="center"  // Center content vertically
                                justifyContent="center"  // Center content horizontally
                                w="100%"
                                h="100%"
                                rounded="lg"
                                overflow="auto"  // Allow horizontal scrolling
                            >
                                <Stack
                                flex='auto'
                                backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "gray.800"}
                                boxShadow="md"
                                w="100%"
                                h="100%"
                                overflow='auto'
                                alignItems="center" // Add this line to center content horizontally
                                justifyContent="center" // Add this line to center content vertically
                                >
                                <Card h='100%' overflowY='auto'>
                                    <CardBody h='100%'>
                                    <Image
                                        src={colorMode === 'light' ? JournalLight : Journal}
                                        alt='Journal Screen'
                                        borderRadius='lg'
                                    />
                                    <Stack display='flex' alignItems='center' mt='6' spacing='3'>
                                        <Heading size='md'>Journal</Heading>
                                        <Text paddingTop='5px' h='175px'>
                                        Your Journal. Your Diary. Your Sandbox.
                                        <br></br>
                                        <br></br>
                                        Use this as your area to strategize, put your thoughts onto paper and save valuable information/link/photos for later.
                                        We use a text editor that is full of features for your to use to your aid as you save and update your entries.
                                        <br></br>
                                        </Text>
                                    </Stack>
                                    </CardBody>
                                </Card>
                                </Stack>
                            </Box>
                        </Box>
                    </TabPanel>
                </TabPanels>
                <TabList overflowX='auto' flexWrap='wrap'>
                    <Tab onClick={() => setTabIndex(0)}>Summary Page</Tab>
                    <Tab onClick={() => setTabIndex(1)}>Trade Management</Tab>
                    <Tab onClick={() => setTabIndex(2)}>Calendar View</Tab>
                    <Tab onClick={() => setTabIndex(3)}>Journal</Tab>
                </TabList>
            </Tabs>
        </VStack>
        
        <Box 
            w='100%'
            h='100%' 
            justify="space-between" 
            bg={colorMode === 'light' ? "blue.500" : "blue.200"}
        >
            <HStack alignItems="start" overflowX="scroll" overflowY="scroll">
                <VStack className={colorMode === 'light' ? "footer" : "footerdark"} w='50%' spacing={2} >
                    <Text>
                        About Us
                    </Text>
                    <div className={colorMode === 'light' ? "footertext" : "footertextdark"}>
                        <Text as='samp'>
                            MyTradingTracker is a free to use personal tool to help traders of ALL experience levels.
                            Our tool offers the ability to log and review trades, analyze your trading progress over various timeframes and filters, 
                            view your month by month progress and even log your thoughts via journal reflection among much more! Give us a try for free and
                            if you don't find it to improve your trading experience simply delete your account! 
                        </Text>
                    </div>
                </VStack>
                
                <VStack className={colorMode === 'light' ? "footer" : "footerdark"}>
                    <Text >
                        Contact Us
                    </Text>
                    <List className={colorMode === 'light' ? "footerlist" : "footerlistdark"} spacing={2}>
                        <ListItem>
                            <Text as='samp'>
                                <ListIcon as={HiOutlineMail} />
                                Email: <a href="mailto:mytradingtrackerapp@gmail.com">mytradingtrackerapp@gmail.com</a>
                            </Text>
                        </ListItem>
                        <ListItem>
                            <Text as='samp'>
                                <ListIcon as={BsFilePersonFill} />
                                Social Media: Coming Soon!
                            </Text>
                        </ListItem>
                    </List>
                </VStack>

                <VStack className={colorMode === 'light' ? "footer" : "footerdark"}>
                    <Text >
                        Our Features
                    </Text>
                    <List className={colorMode === 'light' ? "footerlist" : "footerlistdark"} spacing={2}>
                        <ListItem>
                            <Text as='samp'>
                                <ListIcon as={IoAnalyticsSharp} />
                                <a href="tab-panels" onClick={(e) => handleAnchorClick(e, 'tab-panels', 0)}>
                                Analytics
                                </a>
                            </Text>
                        </ListItem>
                        <ListItem onClick={(e) => setTabIndex(1)}>
                            <Text as='samp'>
                                <ListIcon as={FiMonitor} />
                                <a href="tab-panels" onClick={(e) => handleAnchorClick(e, 'tab-panels', 1)}>
                                Trade Management
                                </a>
                            </Text>
                        </ListItem>
                        <ListItem onClick={(e) => setTabIndex(2)}>
                            <Text as='samp'>
                                <ListIcon as={BsCalendarEvent} />
                                <a href="tab-panels" onClick={(e) => handleAnchorClick(e, 'tab-panels', 2)}>
                                Profit and Loss Calendar
                                </a>
                            </Text>
                        </ListItem>
                        <ListItem onClick={(e) => setTabIndex(3)}>
                            <Text as='samp'>
                                <ListIcon as={BsJournal} />
                                <a href="tab-panels" onClick={(e) => handleAnchorClick(e, 'tab-panels', 3)}>
                                Journal
                                </a>
                            </Text>
                        </ListItem>
                    </List>
                </VStack>
            </HStack>
        </Box>
      </Stack>
    </Flex>
  </Flex>
  
  )
}