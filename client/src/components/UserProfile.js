import React, { useState } from 'react';
import {
  Flex,
  Text,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  StackDivider,
  InputLeftElement,
  chakra,
  Select,
  Box,
  Link,
  Avatar,
  FormControl,
  FormHelperText,
  Badge,
  Center,
  InputRightElement,
} from "@chakra-ui/react";
import { useSelector, useDispatch } from "react-redux";
import { Link as RouterLink, useNavigate } from "react-router-dom"
import { logout, update } from '../store/auth';
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import states from "../data/states";

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function UserProfile({ user }) {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const user_id = user.user_id;
  const [selectPage, setSelectPage] = useState(true);
  const [updateInfo, selectUpdateInfo] = useState(false);

  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [birthday, setBirthday] = useState("");
  const [email, setEmail] = useState("");
  const [street_address, setStreetAddress] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [country, setCountry] = useState("");

  function clearFormStates() {
    setFirstName("");
    setLastName("");
    setBirthday("");
    setEmail("");
    setStreetAddress("");
    setCity("");
    setState("");
    setCountry("");
  }

  const handleGotoUpdate = (e) => {
    e.preventDefault();
    setSelectPage(false);
    selectUpdateInfo(true);
  };

  const handleLogout = (e) => {
    e.preventDefault();
    setSelectPage(true);
    selectUpdateInfo(false);
    dispatch(logout());
    navigate("/");
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    await dispatch(
      update({
        user_id,
        first_name,
        last_name,
        email,
        birthday,
        street_address,
        city,
        state,
        country
      })
    );
    clearFormStates();
    setSelectPage(true);
    selectUpdateInfo(false);
  }

  const handleCancel = (e) => {
    e.preventDefault();
    clearFormStates();
    setSelectPage(true);
    selectUpdateInfo(false);
  }

    // grabbing current date to set a max to the birthday input
    const currentDate = new Date();
    let [month, day, year] = currentDate.toLocaleDateString().split("/");
    // input max field must have 08 instead of 8
    month = month.length === 2 ? month : "0" + month;
    day = day.length === 2 ? day : "0" + day;
    const maxDate = year + "-" + month + "-" + day;

  return (
    selectPage ? (
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
          <Heading color="teal.400">Profile Page</Heading>
          <Box minW={{ base: "90%", md: "250px" }} rounded="lg" overflow="hidden">
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
            >

              <Box display="flex" justifyContent={"left"}>
              <Badge width="100px" variant='outline' borderRadius='12' color="teal.400" >
                <Center h='40px'>
                  Full Name
                </Center>
              </Badge>
              <Text as='b'>
                <Center h='40px'>
                  &nbsp;: {user.first_name} {user.last_name}
                </Center>
              </Text>
              </Box>
              

              <Box display="flex" justifyContent={"left"}>
              <Badge width="100px" variant='outline' borderRadius='12' color="teal.400" >
                <Center h='40px'>
                  Birthday
                </Center>
              </Badge>
              <Text as='b'>
                <Center h='40px'>
                  &nbsp;: {user.birthday}&nbsp;&nbsp;
                </Center>
              </Text>
              </Box>
             
              <Box display="flex">
              <Badge width="100px" variant='outline' borderRadius='12' color="teal.400" >
                <Center h='40px'>
                  Email
                </Center>
              </Badge>
              <Text as='b'>
                <Center h='40px'>
                  &nbsp;: {user.email}
                </Center>
              </Text>
              </Box>
              
            <Box display="flex" justifyContent={"left"}>
              <Badge width="100px" variant='outline' borderRadius='12' color="teal.400" >
                <Center h='40px'>
                  Address
                </Center>
              </Badge>
              <Text as='b'>
                <Center h='40px'>
                  &nbsp;: {user.street_address}, {user.city}, {user.state}, {user.country}
                </Center>
              </Text>
            </Box>
              <Button  borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full" 
                onClick={handleGotoUpdate}>
                Update Information
              </Button>
              <Button  borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full" 
                onClick={handleLogout}>
                Logout
              </Button>
            </Stack>
          </Box>
          </Stack>
        </Flex>
    ) : updateInfo ? (
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
          <Heading color="teal.400">Update Information</Heading>
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
                    placeholder={user.first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                  />
                </FormControl>
                <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Last Name *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={user.last_name}
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </FormControl>
              </Box>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Email *
                </FormHelperText>
                <Input type="name" placeholder={user.email} onChange={(e) => setEmail(e.target.value)} />
              </FormControl>

              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Birthday *
                </FormHelperText>
                <InputGroup>
                  <Input
                    placeholder={user.birthday}
                    onFocus={(e) => (e.target.type = "date")}
                    onBlur={(e) => (e.target.type = "text")}
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
                    placeholder={user.street_address}
                    onChange={(e) => setStreetAddress(e.target.value)}
                  />
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    City *
                  </FormHelperText>
                  <Input
                    type="name"
                    placeholder={user.city}
                    onChange={(e) => setCity(e.target.value)}
                  />
              </FormControl>
              </Box>

              <Box display="flex">
              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    State *
                  </FormHelperText>
                  <Select placeholder={user.state} onChange={(e) => setState(e.target.value)}>
                    {states.map((state) => (<option key={state}>{state}</option>))}
                  </Select>
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Country *
                  </FormHelperText>
                  <Select placeholder={user.country} onChange={(e) => setCountry(e.target.value)}>
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
                onClick={handleUpdate}
              >
                Confirm Update
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
          </Box>
            
          </Stack>
        </Flex>   
    ) : (
      <Heading textAlign='center' backgroundColor="gray.200"> Error</Heading>
    )
  )
}