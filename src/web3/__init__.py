repay_event_sign = self.web3.keccak(text="Repay(address,address,address,uint256)").hex()
withdraw_event_sign = self.web3.keccak(text="Withdraw(address,address,address,uint256)").hex()
deposit_event_sign = self.web3.keccak(text="Deposit(address,address,address,uint256,uint16)").hex()
borrow_event_sign = self.web3.keccak(text="Borrow(address,address,address,uint256,uint256,uint16)").hex()

print(repay_event_sign)
print(withdraw_event_sign)
print(deposit_event_sign)
print(borrow_event_sign)

while True:
    try:
        abc = self.web3.eth.filter(
            {'fromBlock': 11627375, 'toBlock': 11637375, 'address': pool_address})
        event_logs = self.web3.eth.getFilterLogs(abc.filter_id)
        print(event_logs)

        count = 0
        for item in event_logs:
            event_sign_lower = f"0x{convert_hex_to_string(item.topics[0]).lower()}"
            if event_sign_lower in [repay_event_sign, withdraw_event_sign, deposit_event_sign,
                                    borrow_event_sign]:
                count += 1
        print("1223344gjhkhlgjh", count)
        break
    except Exception as error:
        trava_logger.error(f"{error}")
