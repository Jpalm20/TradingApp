import React, { useEffect, useState } from 'react';
import '../styles/profile.css';
import { FiSettings } from "react-icons/fi";
import moment from 'moment'; 
import 'moment-timezone';
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
  SimpleGrid,
  FormLabel,
  Box,
  Icon,
  Toast,
  useToast,
  Link,
  Switch,
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
  ButtonGroup,
  useColorMode 
} from "@chakra-ui/react";
import { useSelector, useDispatch } from "react-redux";
import { Link as RouterLink, useNavigate } from "react-router-dom"
import { logout, update, deleteUser, changePassword, expiredLogout, toggleAvTracking, toggleEmailOptin, toggleFeatureFlags } from '../store/auth';
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
  const { preferences } = useSelector((state) => state.auth); 
  const hasPreferences = ((preferences && Object.keys(preferences).length > 0) ? (true):(false)); 
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

  const [settingsPopUp, setSettingsPopUp] = useState(false);
  
  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = React.useRef();

  const authLoading = useSelector((state) => state.auth.loading);
  const tradeLoading = useSelector((state) => state.trade.loading);

  const { colorMode, toggleColorMode } = useColorMode();

  useEffect(() => {
    evaluateSuccess();
  }, [success]); 

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }


  const evaluateSuccess = () => {
    if(success === true && user.result === "User Edited Successfully" && !(info && info.result && info.result === "Password Successfully Changed")){
      clearFormStates();
      setSelectPage(true);
      selectUpdateInfo(false);
      setToastMessage(user.result);
    }else if(success === true && info && info.result && info.result === "Password Successfully Changed"){
      setToastMessage(info.result);
      setChangePwAlertDialog(false);
      handleLogout();
      onClose();
    }else if (success === true && info && info.result && info.result === "User Successfully Deleted"){
      setToastMessage(info.result);
      dispatch(expiredLogout());    
      setDeleteAlertDialog(false);
      onClose();
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
    const savedUserInfo = window.localStorage.getItem('updateUserInfo');
    if (savedUserInfo) {
      const userInfo = JSON.parse(savedUserInfo);
      setFirstName(userInfo.first_name || "");
      setLastName(userInfo.last_name || "");
      setBirthday(userInfo.birthday || "");
      setEmail(userInfo.email || "");
      setStreetAddress(userInfo.street_address || "");
      setCity(userInfo.city || "");
      setState(userInfo.state || "");
      setCountry(userInfo.country || "");
      // Clear the saved info after loading it
      //window.localStorage.removeItem('userInfo');
    }
  }, []); // Empty dependency array means this runs once on mount

  function clearFormStates() {
    setFirstName("");
    setLastName("");
    setBirthday("");
    setEmail("");
    setStreetAddress("");
    setCity("");
    setState("");
    setCountry("");
    window.localStorage.removeItem('updateUserInfo');
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
        curr_pass,
        new_pass_1,
        new_pass_2
      })
    );
  };

  const handleCancelChangePw = (e) => {
    setChangePwAlertDialog(false);
    onClose();
  };

  const handleSettingsPopUp = (e) => {
    setSettingsPopUp(true);
  };

  const handleCloseSettingsPopUp = (e) => {
    setSettingsPopUp(false);
  };

  const handleToggleAvTracking = async (e) => {
    //await dispatch(toggleAvTracking());
    const flags = ["account_value_optin"];
    await dispatch(
      toggleFeatureFlags({
        flags
      })
    );
  }

  const handleToggleEmailOptin = async (e) => {
    //await dispatch(toggleEmailOptin());
    const flags = ["email_optin"];
    await dispatch(
      toggleFeatureFlags({
        flags
      })
    );
  }

  const handleLogout = async () => {
    setSelectPage(true);
    selectUpdateInfo(false);
    await dispatch(logout());
    navigate("/login");
  };

  const handleDeleteButton = (e) => {
    setDeleteAlertDialog(true);
    onOpen();
  };

  const handleConfirmDelete = async (e) => {
    e.preventDefault();
    await dispatch(deleteUser());
  };

  const handleCancelDelete = (e) => {
    setDeleteAlertDialog(false);
    onClose();
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    const updateUserInfo = {
      first_name,
      last_name,
      email,
      birthday,
      street_address,
      city,
      state,
      country,
    };
    await dispatch(
      update({
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
    //clearFormStates();
    window.localStorage.setItem('updateUserInfo', JSON.stringify(updateUserInfo));
  }

  const handleCancel = (e) => {
    e.preventDefault();
    clearFormStates();
    setSelectPage(true);
    selectUpdateInfo(false);
  }

  const handleClear = (e) => {
    e.preventDefault();
    clearFormStates();
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
          backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
          justifyContent="center"
          alignItems="center"
          overflow="scroll"
        >
          <Stack 
            class='profilestack'
          >
          <Avatar class='avatar' />
          <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>Profile Information</Heading>
          <Box minW={{ base: "90%", md: "500px" }} rounded="lg" overflow="hidden" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          {authLoading && !changepwdialog && !deletealertdialog && !settingsPopUp? 
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
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor={colorMode === 'light' ? "whiteAlpha.900" : "whiteAlpha.100"}
              boxShadow="md"
            >

              <Card>
              <div class='top-right-component'>
                <Icon padding="5px" as={FiSettings} boxSize={8} onClick={handleSettingsPopUp}/>
                <AlertDialog
                  motionPreset='slideInBottom'
                  isOpen={settingsPopUp}
                  leastDestructiveRef={cancelRef}
                  onClose={e => handleCloseSettingsPopUp(e)}
                  isCentered={true}
                  closeOnOverlayClick={true}
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
                  <AlertDialogContent maxWidth='350px' minWidth='300px' overflowX='auto' minHeight='250px'>
                    <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                      Settings
                    </AlertDialogHeader>

                    <AlertDialogBody display="flex" flexDirection="column" alignItems="center" justifyContent="center">
                    <SimpleGrid rows={1}>
                      <FormLabel paddingBottom={1} display="flex" alignItems="center">
                        <Text>{colorMode === 'light' ? 'Light' : 'Dark'} Mode</Text>
                        <Switch marginLeft={3} isChecked={colorMode === 'light' ? false : true} onChange={toggleColorMode}/>
                      </FormLabel>

                      <FormLabel display="flex" alignItems="center">
                        <Text>Balance Tracking {hasPreferences && preferences.account_value_optin === 1 ? 'On' : 'Off'}</Text>
                        <Switch marginLeft={3} isChecked={hasPreferences && preferences.account_value_optin === 1 ? true : false} onChange={handleToggleAvTracking}/>
                      </FormLabel>

                      <FormLabel display="flex" alignItems="center">
                        <Text>Email Alerts {hasPreferences && preferences.email_optin === 1 ? 'On' : 'Off'}</Text>
                        <Switch marginLeft={3} isChecked={hasPreferences && preferences.email_optin === 1 ? true : false} onChange={handleToggleEmailOptin}/>
                      </FormLabel>
                    </SimpleGrid>
                    </AlertDialogBody>

                    <AlertDialogFooter>
                      <Button ref={cancelRef} onClick={handleCloseSettingsPopUp}>
                        Done
                      </Button>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                  </AlertDialogOverlay>
                }
                </AlertDialog>
              </div>
                <CardBody>
                  <Stack divider={<StackDivider />} spacing='3'>
                    {user.first_name !== "" && user.last_name !== "" ? (
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Full Name
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.first_name} {user.last_name}
                      </Text>
                    </Box>
                    ) : (
                      null
                    )}
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Email Address
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.email}
                      </Text>
                    </Box>
                    {user.birthday !== "" ? (
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Birthday
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.birthday}&nbsp;&nbsp;
                      </Text>
                    </Box>
                    ) : (
                      null
                    )}
                    {user.street_address !== "" && user.city !== "" && user.state !== "" && user.country !== "" ? (
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Address
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {user.street_address}, {user.city}, {user.state}, {user.country}
                      </Text>
                    </Box>
                    ) : (
                      null  
                    )}
                    <Box>
                      <Heading size='xs' textTransform='uppercase'>
                        Member Since
                      </Heading>
                      <Text pt='2' fontSize='sm'>
                        {returnInTZ(user.created_at)}
                      </Text>
                    </Box>
                  </Stack>
                </CardBody>
              </Card>
              <HStack>
              <Button  borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full" 
                onClick={handleGotoUpdate}>
                Update Information
              </Button>
              <Button  borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full" 
                onClick={handleChangePassword}>
                Change Password
              </Button>
              </HStack>
              <Button  borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
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
                  Are you sure? <br></br> <br></br> You can't undo this action afterwards. All User data and Trade information will be lost. 
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
                  <Button colorScheme='blue' onClick={e => handleConfirmChangePw(e)} ml={3}>
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
          backgroundColor={colorMode === 'light' ? "gray.200" : "gray.800"}
          justifyContent="center"
          alignItems="center"
          overflow="scroll"
        >
          <Stack
            class='profilestack'
          >
          <Avatar class='avatar' />
          <Heading class={colorMode === 'light' ? 'profileheader' : 'profileheaderdark'}>Update Information</Heading>
          <Box minW={{ base: "90%", md: "468px" }} rounded="lg" overflow="hidden" style={{ boxShadow: '2px 4px 4px rgba(0,0,0,0.2)' }}>
          {authLoading && !changepwdialog && !deletealertdialog? 
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
                    First Name *
                  </FormHelperText>
                  <Input
                    type="name"
                    value={first_name}
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
                    value={last_name}
                    placeholder={user.last_name}
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </FormControl>
              </Box>
              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Email *
                </FormHelperText>
                <Input value={email} type="name" placeholder={user.email} onChange={(e) => setEmail(e.target.value)} />
              </FormControl>

              <FormControl>
                <FormHelperText mb={2} ml={1}>
                  Birthday *
                </FormHelperText>
                <InputGroup>
                  <Input
                    value={birthday} 
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
                    value={street_address} 
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
                    value={city} 
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
                  <Select value={state} onChange={(e) => setState(e.target.value)}>
                    <option value="" disabled selected>{user.state}</option>
                    {states.map((state) => (<option key={state}>{state}</option>))}
                  </Select>
              </FormControl>

              <FormControl>
                  <FormHelperText mb={2} ml={1}>
                    Country *
                  </FormHelperText>
                  <Select value={country} onChange={(e) => setCountry(e.target.value)}>
                    <option value="" disabled selected>{user.country}</option>
                    <option value="Afghanistan">Afghanistan</option>
                    <option value="Albania">Albania</option>
                    <option value="Algeria">Algeria</option>
                    <option value="American Samoa">American Samoa</option>
                    <option value="Andorra">Andorra</option>
                    <option value="Angola">Angola</option>
                    <option value="Anguilla">Anguilla</option>
                    <option value="Antartica">Antarctica</option>
                    <option value="Antigua and Barbuda">Antigua and Barbuda</option>
                    <option value="Argentina">Argentina</option>
                    <option value="Armenia">Armenia</option>
                    <option value="Aruba">Aruba</option>
                    <option value="Australia">Australia</option>
                    <option value="Austria">Austria</option>
                    <option value="Azerbaijan">Azerbaijan</option>
                    <option value="Bahamas">Bahamas</option>
                    <option value="Bahrain">Bahrain</option>
                    <option value="Bangladesh">Bangladesh</option>
                    <option value="Barbados">Barbados</option>
                    <option value="Belarus">Belarus</option>
                    <option value="Belgium">Belgium</option>
                    <option value="Belize">Belize</option>
                    <option value="Benin">Benin</option>
                    <option value="Bermuda">Bermuda</option>
                    <option value="Bhutan">Bhutan</option>
                    <option value="Bolivia">Bolivia</option>
                    <option value="Bosnia and Herzegowina">Bosnia and Herzegowina</option>
                    <option value="Botswana">Botswana</option>
                    <option value="Bouvet Island">Bouvet Island</option>
                    <option value="Brazil">Brazil</option>
                    <option value="British Indian Ocean Territory">British Indian Ocean Territory</option>
                    <option value="Brunei Darussalam">Brunei Darussalam</option>
                    <option value="Bulgaria">Bulgaria</option>
                    <option value="Burkina Faso">Burkina Faso</option>
                    <option value="Burundi">Burundi</option>
                    <option value="Cambodia">Cambodia</option>
                    <option value="Cameroon">Cameroon</option>
                    <option value="Canada">Canada</option>
                    <option value="Cape Verde">Cape Verde</option>
                    <option value="Cayman Islands">Cayman Islands</option>
                    <option value="Central African Republic">Central African Republic</option>
                    <option value="Chad">Chad</option>
                    <option value="Chile">Chile</option>
                    <option value="China">China</option>
                    <option value="Christmas Island">Christmas Island</option>
                    <option value="Cocos Islands">Cocos (Keeling) Islands</option>
                    <option value="Colombia">Colombia</option>
                    <option value="Comoros">Comoros</option>
                    <option value="Congo">Congo</option>
                    <option value="Congo">Congo, the Democratic Republic of the</option>
                    <option value="Cook Islands">Cook Islands</option>
                    <option value="Costa Rica">Costa Rica</option>
                    <option value="Cota D'Ivoire">Cote d'Ivoire</option>
                    <option value="Croatia">Croatia (Hrvatska)</option>
                    <option value="Cuba">Cuba</option>
                    <option value="Cyprus">Cyprus</option>
                    <option value="Czech Republic">Czech Republic</option>
                    <option value="Denmark">Denmark</option>
                    <option value="Djibouti">Djibouti</option>
                    <option value="Dominica">Dominica</option>
                    <option value="Dominican Republic">Dominican Republic</option>
                    <option value="East Timor">East Timor</option>
                    <option value="Ecuador">Ecuador</option>
                    <option value="Egypt">Egypt</option>
                    <option value="El Salvador">El Salvador</option>
                    <option value="Equatorial Guinea">Equatorial Guinea</option>
                    <option value="Eritrea">Eritrea</option>
                    <option value="Estonia">Estonia</option>
                    <option value="Ethiopia">Ethiopia</option>
                    <option value="Falkland Islands">Falkland Islands (Malvinas)</option>
                    <option value="Faroe Islands">Faroe Islands</option>
                    <option value="Fiji">Fiji</option>
                    <option value="Finland">Finland</option>
                    <option value="France">France</option>
                    <option value="France Metropolitan">France, Metropolitan</option>
                    <option value="French Guiana">French Guiana</option>
                    <option value="French Polynesia">French Polynesia</option>
                    <option value="French Southern Territories">French Southern Territories</option>
                    <option value="Gabon">Gabon</option>
                    <option value="Gambia">Gambia</option>
                    <option value="Georgia">Georgia</option>
                    <option value="Germany">Germany</option>
                    <option value="Ghana">Ghana</option>
                    <option value="Gibraltar">Gibraltar</option>
                    <option value="Greece">Greece</option>
                    <option value="Greenland">Greenland</option>
                    <option value="Grenada">Grenada</option>
                    <option value="Guadeloupe">Guadeloupe</option>
                    <option value="Guam">Guam</option>
                    <option value="Guatemala">Guatemala</option>
                    <option value="Guinea">Guinea</option>
                    <option value="Guinea-Bissau">Guinea-Bissau</option>
                    <option value="Guyana">Guyana</option>
                    <option value="Haiti">Haiti</option>
                    <option value="Heard and McDonald Islands">Heard and Mc Donald Islands</option>
                    <option value="Holy See">Holy See (Vatican City State)</option>
                    <option value="Honduras">Honduras</option>
                    <option value="Hong Kong">Hong Kong</option>
                    <option value="Hungary">Hungary</option>
                    <option value="Iceland">Iceland</option>
                    <option value="India">India</option>
                    <option value="Indonesia">Indonesia</option>
                    <option value="Iran">Iran (Islamic Republic of)</option>
                    <option value="Iraq">Iraq</option>
                    <option value="Ireland">Ireland</option>
                    <option value="Israel">Israel</option>
                    <option value="Italy">Italy</option>
                    <option value="Jamaica">Jamaica</option>
                    <option value="Japan">Japan</option>
                    <option value="Jordan">Jordan</option>
                    <option value="Kazakhstan">Kazakhstan</option>
                    <option value="Kenya">Kenya</option>
                    <option value="Kiribati">Kiribati</option>
                    <option value="Democratic People's Republic of Korea">Korea, Democratic People's Republic of</option>
                    <option value="Korea">Korea, Republic of</option>
                    <option value="Kuwait">Kuwait</option>
                    <option value="Kyrgyzstan">Kyrgyzstan</option>
                    <option value="Lao">Lao People's Democratic Republic</option>
                    <option value="Latvia">Latvia</option>
                    <option value="Lebanon">Lebanon</option>
                    <option value="Lesotho">Lesotho</option>
                    <option value="Liberia">Liberia</option>
                    <option value="Libyan Arab Jamahiriya">Libyan Arab Jamahiriya</option>
                    <option value="Liechtenstein">Liechtenstein</option>
                    <option value="Lithuania">Lithuania</option>
                    <option value="Luxembourg">Luxembourg</option>
                    <option value="Macau">Macau</option>
                    <option value="Macedonia">Macedonia, The Former Yugoslav Republic of</option>
                    <option value="Madagascar">Madagascar</option>
                    <option value="Malawi">Malawi</option>
                    <option value="Malaysia">Malaysia</option>
                    <option value="Maldives">Maldives</option>
                    <option value="Mali">Mali</option>
                    <option value="Malta">Malta</option>
                    <option value="Marshall Islands">Marshall Islands</option>
                    <option value="Martinique">Martinique</option>
                    <option value="Mauritania">Mauritania</option>
                    <option value="Mauritius">Mauritius</option>
                    <option value="Mayotte">Mayotte</option>
                    <option value="Mexico">Mexico</option>
                    <option value="Micronesia">Micronesia, Federated States of</option>
                    <option value="Moldova">Moldova, Republic of</option>
                    <option value="Monaco">Monaco</option>
                    <option value="Mongolia">Mongolia</option>
                    <option value="Montserrat">Montserrat</option>
                    <option value="Morocco">Morocco</option>
                    <option value="Mozambique">Mozambique</option>
                    <option value="Myanmar">Myanmar</option>
                    <option value="Namibia">Namibia</option>
                    <option value="Nauru">Nauru</option>
                    <option value="Nepal">Nepal</option>
                    <option value="Netherlands">Netherlands</option>
                    <option value="Netherlands Antilles">Netherlands Antilles</option>
                    <option value="New Caledonia">New Caledonia</option>
                    <option value="New Zealand">New Zealand</option>
                    <option value="Nicaragua">Nicaragua</option>
                    <option value="Niger">Niger</option>
                    <option value="Nigeria">Nigeria</option>
                    <option value="Niue">Niue</option>
                    <option value="Norfolk Island">Norfolk Island</option>
                    <option value="Northern Mariana Islands">Northern Mariana Islands</option>
                    <option value="Norway">Norway</option>
                    <option value="Oman">Oman</option>
                    <option value="Pakistan">Pakistan</option>
                    <option value="Palau">Palau</option>
                    <option value="Panama">Panama</option>
                    <option value="Papua New Guinea">Papua New Guinea</option>
                    <option value="Paraguay">Paraguay</option>
                    <option value="Peru">Peru</option>
                    <option value="Philippines">Philippines</option>
                    <option value="Pitcairn">Pitcairn</option>
                    <option value="Poland">Poland</option>
                    <option value="Portugal">Portugal</option>
                    <option value="Puerto Rico">Puerto Rico</option>
                    <option value="Qatar">Qatar</option>
                    <option value="Reunion">Reunion</option>
                    <option value="Romania">Romania</option>
                    <option value="Russia">Russian Federation</option>
                    <option value="Rwanda">Rwanda</option>
                    <option value="Saint Kitts and Nevis">Saint Kitts and Nevis</option> 
                    <option value="Saint LUCIA">Saint LUCIA</option>
                    <option value="Saint Vincent">Saint Vincent and the Grenadines</option>
                    <option value="Samoa">Samoa</option>
                    <option value="San Marino">San Marino</option>
                    <option value="Sao Tome and Principe">Sao Tome and Principe</option> 
                    <option value="Saudi Arabia">Saudi Arabia</option>
                    <option value="Senegal">Senegal</option>
                    <option value="Seychelles">Seychelles</option>
                    <option value="Sierra">Sierra Leone</option>
                    <option value="Singapore">Singapore</option>
                    <option value="Slovakia">Slovakia (Slovak Republic)</option>
                    <option value="Slovenia">Slovenia</option>
                    <option value="Solomon Islands">Solomon Islands</option>
                    <option value="Somalia">Somalia</option>
                    <option value="South Africa">South Africa</option>
                    <option value="South Georgia">South Georgia and the South Sandwich Islands</option>
                    <option value="Span">Spain</option>
                    <option value="SriLanka">Sri Lanka</option>
                    <option value="St. Helena">St. Helena</option>
                    <option value="St. Pierre and Miguelon">St. Pierre and Miquelon</option>
                    <option value="Sudan">Sudan</option>
                    <option value="Suriname">Suriname</option>
                    <option value="Svalbard">Svalbard and Jan Mayen Islands</option>
                    <option value="Swaziland">Swaziland</option>
                    <option value="Sweden">Sweden</option>
                    <option value="Switzerland">Switzerland</option>
                    <option value="Syria">Syrian Arab Republic</option>
                    <option value="Taiwan">Taiwan, Province of China</option>
                    <option value="Tajikistan">Tajikistan</option>
                    <option value="Tanzania">Tanzania, United Republic of</option>
                    <option value="Thailand">Thailand</option>
                    <option value="Togo">Togo</option>
                    <option value="Tokelau">Tokelau</option>
                    <option value="Tonga">Tonga</option>
                    <option value="Trinidad and Tobago">Trinidad and Tobago</option>
                    <option value="Tunisia">Tunisia</option>
                    <option value="Turkey">Turkey</option>
                    <option value="Turkmenistan">Turkmenistan</option>
                    <option value="Turks and Caicos">Turks and Caicos Islands</option>
                    <option value="Tuvalu">Tuvalu</option>
                    <option value="Uganda">Uganda</option>
                    <option value="Ukraine">Ukraine</option>
                    <option value="United Arab Emirates">United Arab Emirates</option>
                    <option value="United Kingdom">United Kingdom</option>
                    <option value="United States">United States</option>
                    <option value="United States Minor Outlying Islands">United States Minor Outlying Islands</option>
                    <option value="Uruguay">Uruguay</option>
                    <option value="Uzbekistan">Uzbekistan</option>
                    <option value="Vanuatu">Vanuatu</option>
                    <option value="Venezuela">Venezuela</option>
                    <option value="Vietnam">Viet Nam</option>
                    <option value="Virgin Islands (British)">Virgin Islands (British)</option>
                    <option value="Virgin Islands (U.S)">Virgin Islands (U.S.)</option>
                    <option value="Wallis and Futana Islands">Wallis and Futuna Islands</option>
                    <option value="Western Sahara">Western Sahara</option>
                    <option value="Yemen">Yemen</option>
                    <option value="Serbia">Serbia</option>
                    <option value="Zambia">Zambia</option>
                    <option value="Zimbabwe">Zimbabwe</option>
                  </Select>
              </FormControl>
              </Box>
              <Button
                borderRadius={0}
                type="submit"
                variant="solid"
                colorScheme="blue"
                width="full"
                onClick={handleUpdate}
              >
                Update
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
        </Flex>   
    ) : (
      <Heading textAlign='center' backgroundColor="gray.200"> Error</Heading>
    )
  )
}