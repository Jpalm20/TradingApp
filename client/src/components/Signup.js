import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { register } from "../store/auth";
import states from "../data/states";
// import { Link } from "react-router-dom";

import {
  Flex,
  Text,
  Heading,
  Input,
  Button,
  InputGroup,
  Toast,
  useToast,
  Stack,
  InputLeftElement,
  chakra,
  Select,
  Box,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function Signup() {
  const dispatch = useDispatch();
  /*
  const [userInfo, setUserInfo] = useState({
    first_name: "",
    last_name: "",
    birthday: "",
    email: "",
    street_address: "",
    city: "",
    state: "",
    country: ""
  })
  */
  const [showPassword, setShowPassword] = useState(false);

  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const toast = useToast();
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);

  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [birthday, setBirthday] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState();
  const [street_address, setStreetAddress] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [country, setCountry] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await dispatch(
      register({
        first_name,
        last_name,
        birthday, //birthday.join("-"), // if its XX-XX-XXXX format
        email,
        password,
        street_address,
        city,
        state,
        country,
      })
    );
  };

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
        variant: 'top-accent',
        status: 'error',
        duration: 3000,
        isClosable: true
      });
    }
    setToastErrorMessage(undefined);
  }, [toastErrorMessage, toast]);

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
        <Heading color="teal.400">Create an account</Heading>
        <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden">
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
                    First Name *
                  </FormHelperText>
                  <Input
                    type="name"
                    onChange={(e) => setFirstName(e.target.value)}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Last Name *
                  </FormHelperText>
                  <Input
                    type="name"
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </FormControl>
              </Box>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Email *
                </FormHelperText>
                <Input type="name" onChange={(e) => setEmail(e.target.value)} />
              </FormControl>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Password *
                </FormHelperText>
                <InputGroup>
                  <Input
                    type={showPassword ? "text" : "password"}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <InputRightElement width="4.5rem">
                    <Button
                      variant={"ghost"}
                      onClick={() =>
                        setShowPassword((showPassword) => !showPassword)
                      }
                    >
                      {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                    </Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>

              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Birthday *
                </FormHelperText>
                <InputGroup>
                  <Input
                    type="date"
                    max={maxDate}
                    min="1900-01-01"
                    onChange={(e) => setBirthday(e.target.value)}
                  />
                </InputGroup>
              </FormControl>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Street Address *
                  </FormHelperText>
                  <Input
                    type="name"
                    onChange={(e) => setStreetAddress(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    City *
                  </FormHelperText>
                  <Input
                    type="name"
                    onChange={(e) => setCity(e.target.value)}
                  />
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    State *
                  </FormHelperText>
                  <Select placeholder='Select State' onChange={(e) => setState(e.target.value)}>
                    {states.map((state) => (<option key={state}>{state}</option>))}
                  </Select>
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Country *
                  </FormHelperText>
                  <Select placeholder='Select Country' onChange={(e) => setCountry(e.target.value)}>
                    <option>United Arab Emirates</option>
                    <option>Nigeria</option>
                    <option>United States</option>
                  </Select>
              </FormControl>
              </Box>

              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={handleSubmit}
              >
                Create account
              </Button>
            </Stack>
          </form>
        </Box>
      </Stack>
      <Box>
        Already have an account?{" "}
        <Link color="teal.500" href="/login">
          Log in
        </Link>
      </Box>
    </Flex>
  );
}