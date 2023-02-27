import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { authenticate } from "../store/auth";
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
  Toast,
  useToast,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Login() {
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const dispatch = useDispatch();
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [errorFlag, setErrorFlag] = useState(false);

  const handleSubmit = async(e) => {
    e.preventDefault();
    await dispatch(authenticate({ email, password }));
  };

  useEffect(() => {
    evaluateError();
  }, [error]); 

  const evaluateError = () => {
    if(error === true){
      setToastErrorMessage(info.response.data.result);
      /*
      setErrorFlag(true);
      setTimeout(() => {
        setErrorFlag(false);
      }, 3000);
      */
    }
    if(error === false){
      /*
      setErrorFlag(false);
      */
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
 

  return (
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
        <Avatar bg="teal.500" />
        <Heading color="teal.400">Welcome</Heading>
        <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden">
          <form>
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor="whiteAlpha.900"
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

              </FormControl>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleSubmit}
              >
                Login
              </Button>
              {handleErrorPopUp()}
            </Stack>
          </form>
        </Box>
      </Stack>
      <Box>
        Don't have an account?{" "}
        <Link color="teal.500" href="/signup">
          Sign Up
        </Link>
      </Box>
    </Flex>
  );
}

// change last Link to react-dom Link (no refresh) or keep Chakra Link (refresh)?