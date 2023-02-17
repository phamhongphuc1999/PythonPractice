pragma solidity 0.5.0;

contract RPC {

    address public owner;
    uint256 public count;
    uint storedData;

    event Increase(address indexed sender, uint256 count);

    constructor() public {
        owner = msg.sender;
    }

    function increase() external {
        count = count + 1;
        emit Increase(msg.sender, count);
    }

    function set_data(uint x) public {
      storedData = x;
   }
   function get_data() public view returns (uint) {
      return storedData;
   }
}
