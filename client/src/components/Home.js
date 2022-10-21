import React, { useEffect, useState, Component } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades } from '../store/auth'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { Chart } from "react-google-charts";
import {
  Flex,
  Text,
  Switch,
  Center,
  Heading,
  Input,
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
  Select,
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
  ChartJS.register(ArcElement, Tooltip, Legend);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trades } = useSelector((state) => state.auth);
  const hasTrades = ((trades.trades && Object.keys(trades.trades).length > 0) ? (true):(false));
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false));

  const [toggleFilter, setToggleFilter] = useState(false);

  const user_id = user.user_id;

  const [trade_id, setTradeID] = useState(null);

  const [filter_trade_type, setFilterTradeType] = useState("");
  const [filter_security_type, setFilterSecurityType] = useState("");
  const [filter_ticker_name, setFilterTickerName] = useState("");
  const [filter_switch_at, setFilterSwitchAT] = useState(true);
  const [filter_switch_ytd, setFilterSwitchYTD] = useState(false);
  const [filter_switch_month, setFilterSwitchMonth] = useState(false);
  const [filter_switch_week, setFilterSwitchWeek] = useState(false);
  const [filter_switch_day, setFilterSwitchDay] = useState(false);


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
    title: "",
    chartArea: {
      width: "100%",
      height: "100%"
    },
    height: "100%",
    width: "100%",
    titlePosition: 'none',
    titleTextStyle: {
      color: '#000',
      bold: true,
      fontSize: 16,
      position: 'centered'
    },
    is3D: true,
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
      position: "none",
    },
  };

  const pieOptionsB = {
    title: "",
    chartArea: {
      width: "100%",
      height: "100%"
    },
    height: "100%",
    width: "100%",
    titlePosition: 'none',
    titleTextStyle: {
      color: '#000',
      bold: true,
      fontSize: 16,
      position: 'centered'
    },
    is3D: true,
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
      position: "none",
    },
  };


  const handleSubmitFilter = (e) => {
    e.preventDefault();
    setToggleFilter(!toggleFilter);
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
        backgroundColor="gray.200"
      >
        <Stack
                p="1rem"
                backgroundColor="whiteAlpha.900"
                align='center'
                rounded="lg"
                borderWidth="1px"
              >
        <Heading color="teal.400" w='full'>
          <Center>
            Home Page
          </Center>
        </Heading>
        </Stack>

       
        
        <Flex
          w='full'
          flexDirection="row"
          flex="auto"
          backgroundColor="gray.200"
        >
          <Stack
            flexDir="column"
            mb="2"
            justifyContent="left"
            alignItems="center"
          >
            <Box flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch">
              <Stack
                spacing={4}
                p="1rem"
                backgroundColor="whiteAlpha.900"
                boxShadow="md"
                align='center'
                minWidth="30vh"
              >
                <Heading color="teal.400" size="md">Filters</Heading>
                <Box width="full">
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select placeholder='Select Trade Type' onChange={(e) => setFilterTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select placeholder='Select Security Type' onChange={(e) => setFilterSecurityType(e.target.value)}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" placeholder='Enter Ticker' onChange={(e) => setFilterTickerName(e.target.value)} />
                </FormControl>
                <Stack align='center' direction='row' paddingTop={5} paddingStart={2} paddingEnd={20} justifyContent="space-between">
                  <Text as="b">All Time</Text>
                  <Switch size='md' colorScheme='teal'/>
                </Stack>
                <Stack align='center' direction='row' paddingTop={5} paddingStart={2} paddingEnd={20} justifyContent="space-between">
                  <Text as="b">YTD</Text>
                  <Switch size='md' colorScheme='teal'/>
                </Stack>
                <Stack align='center' direction='row' paddingTop={5} paddingStart={2} paddingEnd={20} justifyContent="space-between">
                  <Text as="b">Month</Text>
                  <Switch size='md' colorScheme='teal'/>
                </Stack>
                <Stack align='center' direction='row' paddingTop={5} paddingStart={2} paddingEnd={20} justifyContent="space-between">
                  <Text as="b">Week</Text>
                  <Switch size='md' colorScheme='teal'/>
                </Stack>
                <Stack align='center' direction='row' paddingTop={5} paddingStart={2} paddingEnd={20} justifyContent="space-between">
                  <Text as="b">Day</Text>
                  <Switch size='md' colorScheme='teal'/>
                </Stack>

              </Box>
                  <Button colorScheme='teal' width="full" border='1px' borderColor='black' onClick={handleSubmitFilter} >
                    Submit Filter
                  </Button>
              </Stack>
            </Box>
          </Stack>
         
          
          <Stack
            flexDir="column"
            flex="auto"
            mb="2"
          >
          
          <Box flexGrow="1" display="flex" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch">
            <Stack
              flex="auto"
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
              h="full"
              w="full"
              justifyContent="left"
            >
            {{hasTrades} ? (
            <HStack h="full" w="full" align='top'>
            <Box w="50%" borderWidth="1px" rounded="lg" overflow="hidden" alignItems="stretch" >
              <Heading color="teal.400" w='full' paddingTop={4} paddingBottom={4} size="md">
                <Center>
                  Statistics
                </Center>
              </Heading>
            <TableContainer padding={0} maxHeight="100vh" >
              <Table size='sm' variant='striped' colorScheme="facebook">
                    <Tbody>
                        <Tr>
                          <Td># of Trades</Td>
                          <Td isNumeric>{trades.stats.num_trades + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td># of Wins</Td>
                          <Td isNumeric>{trades.stats.num_wins + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td># of Losses</Td>
                          <Td isNumeric>{trades.stats.num_losses + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td># of Day Trades</Td>
                          <Td isNumeric>{trades.stats.num_day + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td># of Swing Trades</Td>
                          <Td isNumeric>{trades.stats.num_swing + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td># of Options Trades</Td>
                          <Td isNumeric>{trades.stats.num_options + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td># of Shares Trades</Td>
                          <Td isNumeric>{trades.stats.num_shares + " Trades"}</Td>
                        </Tr>
                        <Tr>
                          <Td>Largest Win</Td>
                          <Td isNumeric>{formatter.format(trades.stats.largest_win)}</Td>
                        </Tr>
                        <Tr>
                          <Td>Largest Loss</Td>
                          <Td isNumeric>{formatter.format(trades.stats.largest_loss)}</Td>
                        </Tr>
                        <Tr>
                          <Td>Average Win</Td>
                          <Td isNumeric>{formatter.format(trades.stats.avg_win)}</Td>
                        </Tr>
                        <Tr>
                          <Td>Average Loss</Td>
                          <Td isNumeric>{formatter.format(trades.stats.avg_loss)}</Td>
                        </Tr>
                        <Tr>
                          <Td>Total PNL</Td>
                          <Td isNumeric>{formatter.format(trades.stats.total_pnl)}</Td>
                        </Tr>
                        <Tr>
                          <Td>Win %</Td>
                          <Td isNumeric>{percent.format(trades.stats.win_percent/100)}</Td>
                        </Tr>
                    </Tbody>
              </Table>
            </TableContainer>
            </Box>
            <VStack h="full" w="full">
              <Box h="full" w="full" borderWidth="1px" rounded="lg" overflow="hidden" >
                <HStack h="full" w="full">
                  <Box h="full" w="35vh" borderWidth="1px" rounded="lg" overflow="hidden" align="center">
                    <Heading color="teal.400" w='full' paddingTop={4} paddingBottom={4} size="md">
                      <Center>
                        Day Trade vs Swing Trade
                      </Center>
                    </Heading>
                    <List align="center" paddingTop={10}>
                      <ListItem fontSize={16} >
                        <ListIcon as={RiCheckboxBlankFill} color="lightgreen"></ListIcon>
                        Day Trade Win
                      </ListItem>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="green"></ListIcon>
                        Swing Trade Win
                      </ListItem>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="red.200"></ListIcon>
                        Day Trade Loss
                      </ListItem>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="red"></ListIcon>
                        Swing Trade Loss
                      </ListItem>
                    </List>
                  </Box>
                  <Box h="42vh" w="70vh" borderWidth="1px" rounded="lg" alignItems="center">
                    <Chart
                      chartType="PieChart"
                      data={
                        [["Trade Type", "Count"], 
                        ["Day Loss", trades.stats.num_day_loss], 
                        ["Swing Loss", trades.stats.num_swing_loss],
                        ["Day Win", trades.stats.num_day_win],
                        ["Swing Win", trades.stats.num_swing_win]
                      ]}
                      options={pieOptionsA}
                    />
                  </Box>
                </HStack>
              </Box>
              <Box h="full" w="full" borderWidth="1px" rounded="lg" overflow="hidden" >
                <HStack h="full" w="full" >
                  <Box h="full" w="35vh" borderWidth="1px" rounded="lg" overflow="hidden" align="center">
                    <Heading color="teal.400" w='full' paddingTop={4} paddingBottom={4} size="md">
                      <Center>
                        Options vs Shares
                      </Center>
                    </Heading>
                  <List align="center" paddingTop={10}>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="lightgreen"></ListIcon>
                        Options Win
                      </ListItem>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="green"></ListIcon>
                        Shares Win
                      </ListItem>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="red.200"></ListIcon>
                        Options Loss
                      </ListItem>
                      <ListItem fontSize={16}>
                        <ListIcon as={RiCheckboxBlankFill} color="red"></ListIcon>
                        Shares Loss
                      </ListItem>
                    </List>
                  </Box>
                  <Box h="42vh" w="70vh" borderWidth="1px" rounded="lg"  alignItems="center">
                    <Chart
                      chartType="PieChart"
                      data={
                        [["Security Type", "Count"], 
                        ["Options Loss", trades.stats.num_options_loss], 
                        ["Shares Loss", trades.stats.num_shares_loss],
                        ["Options Win", trades.stats.num_options_win],
                        ["Shares Win", trades.stats.num_shares_win]
                      ]}
                      options={pieOptionsB}
                    />
                  </Box>
                </HStack>
              </Box>
            </VStack>
            </HStack>
            ) : (
              <Text>
                No Trade Data To Display
              </Text>
            )}
            </Stack>
          </Box>
          </Stack>
        </Flex>
      </Flex>
  )
}

