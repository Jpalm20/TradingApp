import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { authenticate, confirm2FA } from "../store/auth";
import '../styles/login.css';
import '../styles/landingpage.css';
import '../styles/profile.css';

// import { Link } from "react-router-dom";
import {
  Flex,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Text,
  chakra,
  Box,
  Spinner,
  Toast,
  useToast,
  useColorMode,
  Switch,
  Link,
  Avatar,
  FormControl,
  FormLabel,
  FormHelperText,
  InputRightElement,
  Center,
  HStack,
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Login() {
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const dispatch = useDispatch();
  const { error } = useSelector((state) => state.auth);
  const { success } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const { user } = useSelector((state) => state.auth);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorFlag, setErrorFlag] = useState(false);

  const authLoading = useSelector((state) => state.auth.loading);
  const [open2FA, setOpen2FA] = useState(false);

  const { colorMode, toggleColorMode } = useColorMode();


  const handleSubmit = async(e) => {
    e.preventDefault();
    await dispatch(authenticate({ email, password }));
  };

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  const evaluateSuccess = async () => {
    if(success === true && user?.result === "2FA Enabled, Verification Code Sent to Email"){
      //setToastMessage(user.result);
      setOpen2FA(true);
    }
  }

  useEffect(() => {
    evaluateError();
  }, [error]); 

  const evaluateError = () => {
    if(error === true){
      if (info?.response?.data?.result) {
        setToastErrorMessage(info.response.data.result);
      } else {
        setToastErrorMessage("An unknown error occurred."); // Fallback message
      }
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

  
  const handleErrorPopUp = () => {
    /*
    if(errorFlag === true){
      return (
        <Alert status='error'>
          <AlertIcon />
          <AlertTitle>Login Error</AlertTitle>
          <AlertDescription>{info.response.data.result}</AlertDescription>
        </Alert>
      )
    }
     */
  }

  const handleNewCode = async(e) => {
    e.preventDefault();
    await dispatch(authenticate({ email, password }));
  };

  const handleCancel = async(e) => {
    e.preventDefault();
    setOpen2FA(false);
    setVerificationCode("");
    setEmail("");
    setPassword("");
  };

  const handleSubmit2FA = async(e) => {
    e.preventDefault();
    let code = verificationCode
    await dispatch(confirm2FA({ email, code }));
    setVerificationCode("");
  };
 

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
        flexDir="column"
        mb="2"
        justifyContent="center"
        alignItems="center"
      >
        {!open2FA ?
          <>
          <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'} >Login</Heading>
          <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          {authLoading ? 
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
                <FormControl>
                  <InputGroup>
                    <InputLeftElement
                      pointerEvents="none"
                      children={<CFaUserAlt color="gray.300" />}
                    />
                    <Input
                      type="email"
                      placeholder="email address"
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </InputGroup>
                </FormControl>
                <FormControl>
                  <InputGroup>
                    <InputLeftElement
                      pointerEvents="none"
                      color="gray.300"
                      children={<CFaLock color="gray.300" />}
                    />
                    <Input
                      type={showPassword ? "text" : "password"}
                      placeholder="Password"
                      onChange={(e) => setPassword(e.target.value)}
                    />
                    <InputRightElement width="4.5rem">
                      {/* <Button h="1.75rem" size="sm" onClick={handleShowClick}>
                        {showPassword ? "Hide" : "Show"}
                      </Button> */}
                      <Button
                      variant={'ghost'}
                      onClick={() =>
                        setShowPassword((showPassword) => !showPassword)
                      }>
                      {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                    </Button>
                    </InputRightElement>
                  </InputGroup>
                  
                  <Box display="flex" justifyContent="right" paddingTop={2}>
                    <Link  color="blue.500" href="/resetpassword">
                      Forgot password?
                    </Link>
                  </Box>
                </FormControl>
                <Button
                  borderRadius={0}
                  type="submit"
                  variant="solid"
                  colorScheme="blue"
                  width="full"
                  onClick={handleSubmit}
                >
                  Login
                </Button>
                {handleErrorPopUp()}
              </Stack>
            </form>
          }
          </Box>
          </>
        :
          <>
          <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'} >Login - 2FA</Heading>
          <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          {authLoading ? 
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
                <Center>
                  <Text>
                    Two-Factor Code sent to email:&nbsp;
                    <b>{email}</b>
                  </Text>
                </Center>
                <FormControl>
                  <InputGroup>
                    <InputLeftElement
                      pointerEvents="none"
                      color="gray.300"
                      children={<CFaLock color="gray.300" />}
                    />
                    <Input
                      type="text"
                      placeholder="Enter Verification Code"
                      onChange={(e) => setVerificationCode(e.target.value)}
                    />
                  </InputGroup>
                </FormControl>
                <Center>
                  <Text>
                    Didn't get a code?&nbsp;
                  </Text>
                  <Link color="blue.500" onClick={handleNewCode}>
                    Send Another
                  </Link>
                </Center>
                <Button
                  borderRadius={0}
                  type="submit"
                  variant="solid"
                  colorScheme="blue"
                  width="full"
                  onClick={handleSubmit2FA}
                >
                  Submit
                </Button>
                <Button
                  borderRadius={0}
                  type="submit"
                  variant="solid"
                  colorScheme="blue"
                  width="full"
                  onClick={handleCancel}
                >
                  Cancel
                </Button>
                {handleErrorPopUp()}
              </Stack>
            </form>
          }
          </Box>
          </>
        }
      </Stack>
    </Flex>
  );
}

// change last Link to react-dom Link (no refresh) or keep Chakra Link (refresh)?