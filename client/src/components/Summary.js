import React, { useEffect, useState } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { getTrades } from '../store/auth'
import { Link as RouterLink, useNavigate} from "react-router-dom";
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
  Spinner,
  Heading,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useDisclosure,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  Textarea,
  Select,
  Toast,
  useToast,
  chakra,
  Box,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
  ButtonGroup,
  Badge,
  HStack
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { update, getTrade, reset, deleteTrade } from '../store/trade';

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Summary({ user }) {
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trade } = useSelector((state) => state.trade);
  const { success } = useSelector((state) => state.trade);
  const { trades } = useSelector((state) => state.auth);
  const tradeError = useSelector((state) => state.trade.error);
  const tradeInfo = useSelector((state) => state.trade.info);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const hasTrades = ((trades.trades && Object.keys(trades.trades).length > 0) ? (true):(false));
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false));
  const hasTrade = ((trade && Object.keys(trade).length > 2) ? (true):(false));

  const [editTrade, setEditTrade] = useState(false);
  const [toggleFilter, setToggleFilter] = useState(false);

  const [visib, setVisib] = useState(false);
  function checkVisbility(tradePayload){
    setVisib(tradePayload.security_type === "Options");
  }

  const user_id = user.user_id;

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

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();
  const [deletealertdialog, setDeleteAlertDialog] = useState(false);

  const authLoading = useSelector((state) => state.auth.loading);
  const tradeLoading = useSelector((state) => state.trade.loading);

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  const evaluateSuccess = () => {
    if(success === true && trade.result === "Trade Edited Successfully"){
        setToastMessage(trade.result);
    }
    if(success === true && trade.result === "Trade Successfully Deleted"){
      setToastMessage(trade.result);
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
        variant: 'top-accent',
        status: 'error',
        duration: 3000,
        isClosable: true
      });
    }
    setToastErrorMessage(undefined);
  }, [toastErrorMessage, toast]);

  function clearFormStates() {
    setTradeType("");
    setSecurityType("");
    setTickerName("");
    setTradeDate("");
    setExpiry("");
    setStrike("");
    setBuyValue("");
    setUnits("");
    setRR("");
    setPNL("");
    setPercentWL("");
    setComments("");
  }
  
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
    if (choiceOptions.value === "" && trade.security_type === "Options"){
      setVisib(true);
      setExpiry("");
      setStrike("");
    }else if (choiceOptions.value === "" && trade.security_type === "Shares"){
      setVisib(false);
      setExpiry("");
      setStrike("");
    }
  }

  const handleGotoEdit = async (e, trade_id) => {
    e.preventDefault();
    const res = await dispatch(
      getTrade({
        trade_id
      })
    );
    checkVisbility(res.payload);
    setTradeID(trade_id);
    setEditTrade(true);
  };


  const handleDeleteButton = (e, trade_id) => {
    setTradeID(trade_id);
    setDeleteAlertDialog(true);
    onOpen();
  };

  const handleConfirmDelete = async (e) => {
    e.preventDefault();
    await dispatch(
      deleteTrade({
        trade_id
      })
    );
    await dispatch(
      getTrades({
        user_id
      })
    );
    dispatch(
      reset()      
    );
    setDeleteAlertDialog(false);
    onClose();
  };

  const handleCancelDelete = (e) => {
    setDeleteAlertDialog(false);
    onClose();
  };


  const handleDoneEdit = async (e) => {
    e.preventDefault();
    await dispatch(
        update({
          trade_id,
          user_id,
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
    await dispatch(
      getTrades({
        user_id
      })
    );
    dispatch(
      reset()      
    );
    clearFormStates();
    setEditTrade(false);
  };

  const handleCancel = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    clearFormStates();
    setEditTrade(false);
  }

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
    !editTrade ? (
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
            Trade Summary
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
          {authLoading ?
            <Stack
            flex="auto"
            p="1rem"
            backgroundColor="whiteAlpha.900"
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
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
              h="full"
              w="full"
              justifyContent="left"
            >
            {{hasTrades} ? (
            <TableContainer overflowY="auto" maxHeight="100vh" rounded="lg">
              <Table size='sm' variant='striped' colorScheme='teal'>
                <Thead position="sticky" top={0} bgColor="lightgrey">
                  <Tr>
                    <Th>ID</Th>
                    <Th>Trade<br></br>Type</Th>
                    <Th>Security<br></br>Type</Th>
                    <Th>Ticker</Th>
                    <Th>Close<br></br>Date</Th>
                    <Th>Expiry</Th>
                    <Th>Strike</Th>
                    <Th>Avg<br></br>Price</Th>
                    <Th># of<br></br>Units</Th>
                    <Th>R/R</Th>
                    <Th>PNL</Th>
                    <Th>% W/L</Th>
                    <Th>Comments</Th>
                    <Th></Th>
                  </Tr>
                </Thead>
                    <Tbody>
                      {trades.trades.map((trades, index) => (
                        <Tr>
                          <Td>{trades.trade_id}</Td>
                          <Td>{trades.trade_type}</Td>
                          <Td>{trades.security_type}</Td>
                          <Td>{trades.ticker_name}</Td>
                          <Td>{trades.trade_date}</Td>
                          <Td>{trades.expiry}</Td>
                          <Td isNumeric>{trades.strike}</Td>
                          <Td isNumeric>{trades.buy_value}</Td>
                          <Td isNumeric>{trades.units}</Td>
                          <Td>{trades.rr}</Td>
                          <Td isNumeric>{trades.pnl}</Td>
                          <Td isNumeric>{trades.percent_wl}</Td>
                          <Td whiteSpace="normal">{trades.comments}</Td>
                          <Td>
                            <Button width='100%' height='60%' colorScheme='teal' border='1px' borderColor='black' onClick={e => handleGotoEdit(e, trades.trade_id)}>
                              Edit
                            </Button>
                            <div>
                            <Button width='100%' height='60%' colorScheme='red' border='1px' borderColor='black' onClick={e => handleDeleteButton(e, trades.trade_id)}>
                              Delete
                            </Button>
                            </div>
                          </Td>
                        </Tr>
                      ))}
                    </Tbody>
              </Table>
            </TableContainer>
            ) : (
            <TableContainer>
              <Table size='sm'>
                <Thead>
                  <Tr>
                    <Th>Trade ID</Th>
                    <Th>Trade Type</Th>
                    <Th>Security Type</Th>
                    <Th>Ticker</Th>
                    <Th>Close Date</Th>
                    <Th>Expiry</Th>
                    <Th>Strike</Th>
                    <Th>Avg Price</Th>
                    <Th># of Units</Th>
                    <Th>R/R</Th>
                    <Th>PNL</Th>
                    <Th>% W/L</Th>
                    <Th>Comments</Th>
                    <Th></Th>
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
            {tradeLoading ?
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
        backgroundColor="gray.200"
        justifyContent="center"
        alignItems="center"
      >
        <Stack
          flexDir="column"
          mb="2"
          justifyContent="center"
          alignItems="center"
        >
        <Heading color="teal.400">Update Trade</Heading>
        <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden">
          {tradeLoading ? 
            <Stack
                spacing={4}
                p="1rem"
                backgroundColor="whiteAlpha.900"
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
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
            >
              <Box display="flex">
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Trade Type *
                  </FormHelperText>
                  <Select placeholder={trade.trade_type} onChange={(e) => setTradeType(e.target.value)}>
                    <option>Swing Trade</option>
                    <option>Day Trade</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Security Type *
                  </FormHelperText>
                  <Select id="optionsSelection" placeholder={trade.security_type} onChange={(e) => {changeShowOptions(e.target.value); setSecurityType(e.target.value);}}>
                    <option>Options</option>
                    <option>Shares</option>
                  </Select>
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Ticker *
                  </FormHelperText>
                  <Input type="name" placeholder={trade.ticker_name} onChange={(e) => setTickerName(e.target.value)} />
                </FormControl>
              </Box>
              
              <Box style={{display: visib ? "flex" : "none"}}>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Expiry (Options Only) *
                </FormHelperText>
                <Input
                    placeholder={trade.expiry}
                    onFocus={(e) => (e.target.type = "date")}
                    onBlur={(e) => (e.target.type = "text")}
                    max={maxDate}
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
                    type="name"
                    placeholder={trade.units}
                    onChange={(e) => setUnits(e.target.value)}
                  />
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Risk/Reward Ratio *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={trade.rr}
                    onChange={(e) => setRR(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    PNL *
                  </FormHelperText>
                  <Input
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
                    type="name"
                    placeholder={trade.percent_wl}
                    onChange={(e) => setPercentWL(e.target.value)}
                  />
              </FormControl>
              </Box>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Comments *
                  </FormHelperText>
                  <Textarea placeholder={trade.comments} onChange={(e) => setComments(e.target.value)}/>
              </FormControl>

              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleDoneEdit}
              >
                Update Trade
              </Button>

              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleCancel}
              >
                Cancel
              </Button>
            </Stack>
          </form>
        }
        </Box>
      </Stack>
    </Flex>
    ) 
  )
}
