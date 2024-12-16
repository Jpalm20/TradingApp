import React from 'react';
import ReactSelect from 'react-select';  // Rename this import to avoid conflict with Chakra UI Select
import '../styles/currencyselector.css';
import {useColorMode} from "@chakra-ui/react";

const CurrencySelector = ({ currencies, preferences, handleToggleCurrencyCode }) => {
    const { colorMode } = useColorMode();    
    // Format the currencies for react-select (value/label pair)
    const options = currencies.map((currency) => ({
        value: currency,
        label: currency,
    }));

    // Set the selected currency (if already set in preferences)
    const selectedCurrency = preferences.preferred_currency ? { value: preferences.preferred_currency, label: preferences.preferred_currency } : null;

    // Handle selection change
    const handleChange = (selectedOption) => {
        if(selectedOption !== null){
            handleToggleCurrencyCode(selectedOption ? selectedOption.value : null);
        }
    };

    const customStyles = {
        input: (provided) => ({
        ...provided,
        color: '#717075',  // Input text color
        }),
    };

    const customStylesDark = {
        input: (provided) => ({
        ...provided,
        color: '#DFDFDF',  // Input text color
        }),
    };

    return (
        <ReactSelect
        value={selectedCurrency}           // Controlled selected value
        onChange={handleChange}            // Handle currency selection
        options={options}                  // List of currency options
        isSearchable={true}                // Enable search
        styles={colorMode === 'light' ? customStyles : customStylesDark} 
        className={colorMode === 'light' ? "currency-selector" : "currency-selector-dark"}
        classNamePrefix="currency"
        menuPosition="fixed"
        menuPlacement="auto"
        />
    );
};

export default CurrencySelector;