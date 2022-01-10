//SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    //Types
    //uint256 -> unsigned integer of size 256 bits
    // uint256 myn = 8;
    // bool val = false;
    // string name = "ANshuman";
    // int256 num = -99;
    // //address -> an ethereum address
    // address myadd = 0x94B4e66bB4b9394669Aaa78ea6EEa12d38d985fC;
    // bytes trial = "dog";
    uint256 num;

    struct People {
        uint256 favno;
        string name;
    }
    //Example on creating one person:
    //People public person = People({favno: 8, name:"Anshuman" });
    //Arrays of people
    People[] public people;
    //A Mapping function
    mapping(string => uint256) public nameToFavouriteno;

    function store(uint256 _favno) public returns (uint256){
        num = _favno;
        return num;
    }

    //Trying with a new function

    function retrieve() public view returns (uint256) {
        return num;
    }

    //Function to add a Person to our array
    function addPerson(string memory _name, uint256 _favno) public {
        //WAY - 1:
        //people.push(People({favno: _favno, name: _name}));
        //WAY - 2:
        people.push(People(_favno, _name));
        nameToFavouriteno[_name] = _favno;
    }
}
