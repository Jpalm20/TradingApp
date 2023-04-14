import React, { useEffect, useState } from 'react';
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
  Spinner,
  Box,
  Toast,
  useToast,
  Link,
  Avatar,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useDisclosure,
  FormControl,
  FormHelperText,
  Card, 
  CardBody,
  Badge,
  Center,
  InputRightElement,
  HStack,
} from "@chakra-ui/react";
import { useSelector, useDispatch } from "react-redux";
import { Link as RouterLink, useNavigate } from "react-router-dom"
import { logout, update, deleteUser, changePassword } from '../store/auth';
import { FaUserAlt, FaLock } from "react-icons/fa";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import states from "../data/states";


const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

export default function UserProfile({ user }) {
  const [toastMessage, setToastMessage] = useState(undefined);
  const [toastErrorMessage, setToastErrorMessage] = useState(undefined);
  const { error } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const { success } = useSelector((state) => state.auth);
  const toast = useToast();
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

  const [changepwdialog, setChangePwAlertDialog] = useState(false);
  const [curr_pass, setCurrPass] = useState("");
  const [new_pass_1, setNewPass1] = useState("");
  const [new_pass_2, setNewPass2] = useState("");
  const [showCurrPassword, setShowCurrPassword] = useState(false);
  const [showNewPassword1, setShowNewPassword1] = useState(false);
  const [showNewPassword2, setShowNewPassword2] = useState(false);

  const [deletealertdialog, setDeleteAlertDialog] = useState(false);
  
  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();

  const authLoading = useSelector((state) => state.auth.loading);
  const tradeLoading = useSelector((state) => state.trade.loading);


  useEffect(() => {
    evaluateSuccess();
  }, [success]); 


  const evaluateSuccess = () => {
    if(success === true && user.result === "User Edited Successfully"){
        setToastMessage(user.result);
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

  const handleChangePassword = (e) => {
    setChangePwAlertDialog(true);
    onOpen();
  };

  const handleConfirmChangePw = async (e) => {
    e.preventDefault();
    await dispatch(
      changePassword({
        user_id,
        curr_pass,
        new_pass_1,
        new_pass_2
      })
    );
    handleLogout(e);    
    setChangePwAlertDialog(false);
    onClose();
  };

  const handleCancelChangePw = (e) => {
    setChangePwAlertDialog(false);
    onClose();
  };

  const handleLogout = async (e) => {
    e.preventDefault();
    setSelectPage(true);
    selectUpdateInfo(false);
    await dispatch(logout());
    navigate("/");
  };

  const handleDeleteButton = (e) => {
    setDeleteAlertDialog(true);
    onOpen();
  };

  const handleConfirmDelete = async (e) => {
    e.preventDefault();
    await dispatch(
      deleteUser({
        user_id
      })
    );
    handleLogout(e);    
    setDeleteAlertDialog(false);
    onClose();
  };

  const handleCancelDelete = (e) => {
    setDeleteAlertDialog(false);
    onClose();
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
          <Heading color="teal.400">Profile Information</Heading>
          <Box minW={{ base: "90%", md: "500px" }} rounded="lg" overflow="hidden">
          {authLoading && !changepwdialog && !deletealertdialog? 
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
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
            >

              <Card>
                <CardBody>
                  <Stack divider={<StackDivider />} spacing='3'>
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Full Name
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.first_name} {user.last_name}
                      </Text>
                    </Box>
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Email Address
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.email}
                      </Text>
                    </Box>
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Birthday
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.birthday}&nbsp;&nbsp;
                      </Text>
                    </Box>
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Address
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.street_address}, {user.city}, {user.state}, {user.country}
                      </Text>
                    </Box>
                  </Stack>
                </CardBody>
              </Card>
              <HStack>
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
                onClick={handleChangePassword}>
                Change Password
              </Button>
              </HStack>
              <Button  borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="teal"
                width="full" 
                onClick={handleLogout}>
                Logout
              </Button>
              <Button borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="red"
                width="full"
                onClick={e => handleDeleteButton(e)}>
                Delete Account
              </Button>
            </Stack>
            }
            {deletealertdialog}
              <AlertDialog
              motionPreset='slideInBottom'
              isOpen={deletealertdialog}
              leastDestructiveRef={cancelRef}
              onClose={e => handleCancelDelete(e)}
              isCentered={true}
              closeOnOverlayClick={false}
            >
            {authLoading || tradeLoading ?
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
                  Delete User
                </AlertDialogHeader>

                <AlertDialogBody>
                  Are you sure? You can't undo this action afterwards. All User data and Trade information will be lost.
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
            {changepwdialog}
              <AlertDialog
              motionPreset='slideInBottom'
              isOpen={changepwdialog}
              leastDestructiveRef={cancelRef}
              onClose={e => handleChangePassword(e)}
              isCentered={true}
              closeOnOverlayClick={false}
            >
            {authLoading || tradeLoading ?
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

                <AlertDialogBody>
                  <FormControl>
                    <FormHelperText mb={2} ml={1}>
                      Current Password *
                    </FormHelperText>
                    <InputGroup>
                      <Input
                        type={showCurrPassword ? "text" : "password"}
                        onChange={(e) => setCurrPass(e.target.value)}
                      />
                      <InputRightElement width="4.5rem">
                        <Button
                          variant={"ghost"}
                          onClick={() =>
                            setShowCurrPassword((showCurrPassword) => !showCurrPassword)
                          }
                        >
                          {showCurrPassword ? <ViewIcon /> : <ViewOffIcon />}
                        </Button>
                      </InputRightElement>
                    </InputGroup>
                  </FormControl>
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
                  <Button ref={cancelRef} onClick={e => handleCancelChangePw(e)}>
                    Cancel
                  </Button>
                  <Button colorScheme='teal' onClick={e => handleConfirmChangePw(e)} ml={3}>
                    Change Password
                  </Button>
                </AlertDialogFooter>
              </AlertDialogContent>
              </AlertDialogOverlay>
            }
            </AlertDialog>
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
          {authLoading && !changepwdialog && !deletealertdialog? 
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
          }
          </Box>
            
          </Stack>
        </Flex>   
    ) : (
      <Heading textAlign='center' backgroundColor="gray.200"> Error</Heading>
    )
  )
}