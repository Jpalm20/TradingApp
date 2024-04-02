import React, { useEffect, useState } from 'react'
import { useSelector, useDispatch } from "react-redux";
import { create , reset} from '../store/trade'
import { Link as RouterLink, useNavigate} from "react-router-dom";
import { getTrades, getTradesPage } from '../store/auth';
// import { Link } from "react-router-dom";   
import '../styles/logtrade.css';
import axios from "axios";

import {
  Flex,
  Text,
  Center,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  Textarea,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useColorMode,
  Spinner,
  useDisclosure,
  Select,
  chakra,
  Box,
  Toast,
  useToast,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
  ButtonGroup,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  HStack
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function LogTrade({ user }) {
  const [toastMessage, setToastMessage] = useState(undefined);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { trade } = useSelector((state) => state.trade);
  const { error } = useSelector((state) => state.trade);
  const { info } = useSelector((state) => state.trade);
  const { success } = useSelector((state) => state.trade);
  const tradeLogged = ((trade && Object.keys(trade).length > 2) ? (true):(false));
  const [visib, setVisib] = useState(true);

  const user_id = user.user_id;
  const [trade_type, setTradeType] = useState("");
  const [security_type, setSecurityType] = useState("");
  const [ticker_name, setTickerName] = useState("");
  const [trade_date, setTradeDate] = useState("");
  const [expiry, setExpiry] = useState("");
  const [strike, setStrike] = useState("");
  const [buy_value, setBuyValue] = useState("");
  const [units, setUnits] = useState("");
  const [rr, setRR] = useState("1:1");
  const [pnl, setPNL] = useState("");
  const [percent_wl, setPercentWL] = useState("");
  const [comments, setComments] = useState(""); 
  const cancelRef = React.useRef();
  const { isOpen, onOpen, onClose } = useDisclosure();

  const tradeLoading = useSelector((state) => state.trade.loading);

  const { colorMode, toggleColorMode } = useColorMode();

  const format = (val1,val2) => val1 + ":" + val2;
  const [risk, setRisk] = useState("1");
  const [reward, setReward] = useState("1");

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

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

  const evaluateSuccess = async () => {
    if(success === true && trade.result === "Trade Logged Successfully"){
      clearFormStates();
      setToastMessage(trade.result);
      const filters = {};
      filters.page = 1;
      filters.numrows = 100;
      await dispatch(getTradesPage({ filters }));
      setSearchValue('');
      setSelectedValue('');
      setIsDropdownOpen(false);
      
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

  useEffect(() => {
    const savedTradeInfo = window.localStorage.getItem('tradeInfo');
    if (savedTradeInfo) {
      const tradeInfo = JSON.parse(savedTradeInfo);
      setTradeType(tradeInfo.trade_type || "");
      setSecurityType(tradeInfo.security_type || "");
      setTickerName(tradeInfo.ticker_name || "");
      setTradeDate(tradeInfo.trade_date || "");
      setExpiry(tradeInfo.expiry || "");
      setStrike(tradeInfo.strike || "");
      setBuyValue(tradeInfo.buy_value || "");
      setUnits(tradeInfo.units || "");
      setRR(tradeInfo.rr || "1:1");
      setPNL(tradeInfo.pnl || "");
      setPercentWL(tradeInfo.percent_wl || "");
      setComments(tradeInfo.comments || "");
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
    setRR("1:1");
    setPNL("");
    setPercentWL("");
    setComments("");
    setRisk("1");
    setReward("1");
    window.localStorage.removeItem('tradeInfo');
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

  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    const tradeInfo = {
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
      create({
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
    window.localStorage.setItem('tradeInfo', JSON.stringify(tradeInfo));
  }

  const handleClear = (e) => {
    e.preventDefault();
    clearFormStates();
  }

  const handleCancel = async (e) => {
    e.preventDefault();
    clearFormStates();
    navigate("/summary");
    const filters = {};
    filters.page = 1;
    filters.numrows = 100;
    await dispatch(getTradesPage({ filters }));
    setSearchValue('');
    setSelectedValue('');
    setIsDropdownOpen(false);
  }

  const handleAnswerYes = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    clearFormStates();
    navigate("/logTrade");
  }

  const handleAnswerNo = (e) => {
    e.preventDefault();
    dispatch(
      reset()
    );
    clearFormStates();
    navigate("/summary");
  }

  useEffect(() => {
    calculatePercent();
  }, [pnl, buy_value, units]); 

  const calculatePercent = () => {
    const pnlFloat=parseFloat(pnl);
    const buyValueFloat=parseFloat(buy_value);
    const unitsFloat=parseFloat(units);
    if (!isNaN(pnlFloat) && !isNaN(buyValueFloat) && buyValueFloat !== 0 && !isNaN(unitsFloat) && unitsFloat !== 0) {
      setPercentWL(((pnlFloat/(buyValueFloat*unitsFloat)*100).toFixed(2)));
    }else{
      setPercentWL("");
    }
  }

  const [searchValue, setSearchValue] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedValue, setSelectedValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);


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
      width="100wh"
      height="100vh"
      backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
      justifyContent="center"
      alignItems="center"
    >
      <Stack
        class='profilestack'
      >
        <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>Log Trade</Heading>
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
                onClick={handleSubmit}
              >
                Create Entry
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
      </Stack>
      {tradeLogged}
      <AlertDialog
        motionPreset='slideInBottom'
        isOpen={tradeLogged}
        leastDestructiveRef={cancelRef}
        onClose={e => handleAnswerNo(e)}
        isCentered={true}
        closeOnOverlayClick={false}
      >
        <AlertDialogOverlay>
        <AlertDialogContent>
          <AlertDialogHeader fontSize='lg' fontWeight='bold'>
            Trade Logged Successfully
          </AlertDialogHeader>

          <AlertDialogBody>
            Would You Like to Log Another?
          </AlertDialogBody>

          <AlertDialogFooter>
            <Button colorScheme='blue' onClick={e => handleAnswerYes(e)}>
              Yes
            </Button>
            <Button ref={cancelRef} colorScheme='gray' onClick={e => handleAnswerNo(e)} ml={3}>
              No
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Flex>
  );
}
