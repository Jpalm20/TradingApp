import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { resetPassword , generateResetCode, confirmResetCode} from "../store/auth";
import { Link as RouterLink, useNavigate} from "react-router-dom";
import '../styles/login.css';

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
  useColorMode,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  AlertDialogCloseButton,
  useDisclosure,
  Toast,
  useToast,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
  Center,
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Login() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [new_pass_1, setNewPass1] = useState("");
  const [new_pass_2, setNewPass2] = useState("");
  const [showNewPassword1, setShowNewPassword1] = useState(false);
  const [showNewPassword2, setShowNewPassword2] = useState(false);

  const [enterCode, setEnterCode] = useState(false);
  const [enterPw, setEnterPw] = useState(false);

  const authLoading = useSelector((state) => state.auth.loading);

  const { colorMode, toggleColorMode } = useColorMode();

  const handleSubmit = async(e) => {
    e.preventDefault();
    await dispatch(generateResetCode({ email }));
  };

  const handleSubmitCode = async(e) => {
    e.preventDefault();
    await dispatch(confirmResetCode({ email, code }));
  };

  const handleChangePassword = (e) => {
    setEnterPw(false);
  };

  const handleConfirmChangePw = async (e) => {
    e.preventDefault();
    await dispatch(
      resetPassword({
        code,
        email,
        new_pass_1,
        new_pass_2
      })
    );
    setEnterPw(false);
    setEnterCode(false);
    onClose();
  };

  useEffect(() => {
    evaluateError();
  }, [error]); 

  useEffect(() => {
    evaluateInfo();
  }, [info]); 

  const evaluateError = () => {
    if(error === true){
      setToastErrorMessage(info.response.data.result);
    }
  }

  const evaluateInfo = () => {
    if(info.result === "Reset Code Generated Successfully"){
        setEnterCode(true);
    }
    if(info.result === "Reset Code Verified Successfully"){
        setEnterPw(true);
    }
    if(info.result === "Password Reset Successfully"){
        navigate("/login");
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
        <Heading class={colorMode === 'light' ? 'loginheader' : 'loginheaderdark'}>Reset Your Password</Heading>
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
                    value={email}
                    isDisabled={enterCode}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </InputGroup>
              </FormControl>
              {!enterCode ?
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleSubmit}
              >
                Reset
              </Button>
              :
              <>
              <Center>
                <Text paddingLeft={5} paddingRight={5} textAlign="center" fontSize="md" maxWidth="600px">
                    Reset code sent to {email}. Code expires in 15 minutes.
                </Text>
              </Center>
              <FormControl display="flex" justifyContent="center">
                <InputGroup w="50%">
                  <InputLeftElement
                    pointerEvents="none"
                    color="gray.300"
                    children={<CFaLock color="gray.300" />}
                  />
                  <Input
                    type="text"
                    placeholder="Enter Reset Code"
                    onChange={(e) => setCode(e.target.value)}
                  />
                </InputGroup>
              </FormControl>
              <Center>
                  <Text>
                    Didn't get a code?&nbsp;
                  </Text>
                  <Link color="blue.500" onClick={handleSubmit}>
                    Send Another
                  </Link>
              </Center>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleSubmitCode}
              >
                Submit Code
              </Button>
            <AlertDialog
              motionPreset='slideInBottom'
              isOpen={enterPw}
              leastDestructiveRef={cancelRef}
              onClose={e => handleChangePassword(e)}
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
                  Change Password
                </AlertDialogHeader>
                <AlertDialogCloseButton onClick={e => handleChangePassword(e)}/>
                <AlertDialogBody>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      New Password *
                    </FormHelperText>
                    <InputGroup>
                      <Input
                        type={showNewPassword1 ? "text" : "password"}
                        onChange={(e) => setNewPass1(e.target.value)}
                      />
                      <InputRightElement width="4.5rem">
                        <Button
                          variant={"ghost"}
                          onClick={() =>
                            setShowNewPassword1((showNewPassword1) => !showNewPassword1)
                          }
                        >
                          {showNewPassword1 ? <ViewIcon /> : <ViewOffIcon />}
                        </Button>
                      </InputRightElement>
                    </InputGroup>
                  </FormControl>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Confirm New Password *
                    </FormHelperText>
                    <InputGroup>
                      <Input
                        type={showNewPassword2 ? "text" : "password"}
                        onChange={(e) => setNewPass2(e.target.value)}
                      />
                      <InputRightElement width="4.5rem">
                        <Button
                          variant={"ghost"}
                          onClick={() =>
                            setShowNewPassword2((showNewPassword2) => !showNewPassword2)
                          }
                        >
                          {showNewPassword2 ? <ViewIcon /> : <ViewOffIcon />}
                        </Button>
                      </InputRightElement>
                    </InputGroup>
                  </FormControl>
                </AlertDialogBody>

                <AlertDialogFooter>
                  <Button colorScheme='blue' onClick={e => handleConfirmChangePw(e)} ml={3}>
                    Change Password
                  </Button>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
              </>
              }
            </Stack>
          </form>
        }
        </Box>
      </Stack>
      <Box>
        <Link color="blue.500" href="/login">
            <Text as='u' >
                Return to Log in
            </Text>
        </Link>
      </Box>
    </Flex>
  );
}

// change last Link to react-dom Link (no refresh) or keep Chakra Link (refresh)?