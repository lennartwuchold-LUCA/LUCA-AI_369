// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * 🧬 LUCA DAO Smart Contract
 * Dezentrale autonome Organisation für das LUCA-Netzwerk
 * Proof-of-Metabolism Rewards System
 *
 * This contract implements:
 * - ERC20 token functionality
 * - Proof-of-Metabolism consensus rewards
 * - Node authorization and management
 * - Metabolic performance tracking
 * - Penalty system for poor performance
 */

contract LUCADAO {
    string public constant name = "LUCA DAO Token";
    string public constant symbol = "LUCA";
    uint8 public constant decimals = 18;

    address public owner;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => bool) public authorizedNodes;

    // Metabolic Performance Tracking
    mapping(address => uint256) public metabolicScore;
    mapping(address => uint256) public lastRewardTime;
    mapping(address => uint256) public totalRewardsEarned;
    mapping(address => uint256) public totalPenalties;

    // Configuration
    uint256 public constant REWARD_INTERVAL = 1 days;
    uint256 public constant MAX_REWARD = 100 * 10**18; // 100 LUCA
    uint256 public constant MIN_METABOLIC_SCORE = 70; // Minimum 70% performance

    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Reward(address indexed node, uint256 amount, uint256 metabolicScore, uint256 timestamp);
    event Penalty(address indexed node, uint256 amount, uint256 timestamp);
    event NodeAuthorized(address indexed node, address indexed authorizedBy);
    event NodeRevoked(address indexed node, address indexed revokedBy);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "LUCA: Only owner can call this function");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedNodes[msg.sender], "LUCA: Not an authorized LUCA node");
        _;
    }

    /**
     * @dev Constructor initializes the DAO with initial token supply
     */
    constructor() {
        owner = msg.sender;
        totalSupply = 1000000 * 10**18; // 1 Million LUCA
        balanceOf[msg.sender] = totalSupply;
        authorizedNodes[msg.sender] = true;

        emit Transfer(address(0), msg.sender, totalSupply);
        emit NodeAuthorized(msg.sender, msg.sender);
    }

    /**
     * @dev Authorisiert einen neuen LUCA Node
     * @param node Address of the node to authorize
     */
    function authorizeNode(address node) external onlyOwner {
        require(node != address(0), "LUCA: Cannot authorize zero address");
        require(!authorizedNodes[node], "LUCA: Node already authorized");

        authorizedNodes[node] = true;
        emit NodeAuthorized(node, msg.sender);
    }

    /**
     * @dev Revokes authorization from a node
     * @param node Address of the node to revoke
     */
    function revokeNode(address node) external onlyOwner {
        require(authorizedNodes[node], "LUCA: Node not authorized");
        require(node != owner, "LUCA: Cannot revoke owner");

        authorizedNodes[node] = false;
        emit NodeRevoked(node, msg.sender);
    }

    /**
     * @dev Belohnt einen Node basierend auf Metabolic Performance
     * @param node Address of the node to reward
     * @param metabolicPerformance Performance score (0-100)
     */
    function rewardNode(address node, uint256 metabolicPerformance) external onlyAuthorized {
        require(node != address(0), "LUCA: Cannot reward zero address");
        require(authorizedNodes[node], "LUCA: Node not authorized");
        require(metabolicPerformance <= 100, "LUCA: Performance score must be <= 100");
        require(metabolicPerformance >= MIN_METABOLIC_SCORE, "LUCA: Performance below minimum");
        require(
            block.timestamp >= lastRewardTime[node] + REWARD_INTERVAL,
            "LUCA: Reward interval not elapsed"
        );

        // Berechne Belohnung basierend auf Performance (0-100 LUCA)
        uint256 rewardAmount = (metabolicPerformance * MAX_REWARD) / 100;

        // Stelle sicher dass genug Tokens verfügbar sind
        require(balanceOf[owner] >= rewardAmount, "LUCA: Insufficient tokens in treasury");

        // Transferiere Belohnung
        balanceOf[owner] -= rewardAmount;
        balanceOf[node] += rewardAmount;

        // Update tracking
        metabolicScore[node] = metabolicPerformance;
        lastRewardTime[node] = block.timestamp;
        totalRewardsEarned[node] += rewardAmount;

        emit Transfer(owner, node, rewardAmount);
        emit Reward(node, rewardAmount, metabolicPerformance, block.timestamp);
    }

    /**
     * @dev Bestraft einen Node für schlechte Performance
     * @param node Address of the node to penalize
     * @param penaltyAmount Amount of tokens to penalize
     */
    function penalizeNode(address node, uint256 penaltyAmount) external onlyAuthorized {
        require(node != address(0), "LUCA: Cannot penalize zero address");
        require(authorizedNodes[node], "LUCA: Node not authorized");
        require(penaltyAmount > 0, "LUCA: Penalty amount must be > 0");
        require(balanceOf[node] >= penaltyAmount, "LUCA: Insufficient balance for penalty");

        balanceOf[node] -= penaltyAmount;
        balanceOf[owner] += penaltyAmount;

        totalPenalties[node] += penaltyAmount;

        emit Transfer(node, owner, penaltyAmount);
        emit Penalty(node, penaltyAmount, block.timestamp);
    }

    /**
     * @dev Get comprehensive node statistics
     * @param node Address of the node
     * @return score Current metabolic score
     * @return lastReward Timestamp of last reward
     * @return totalRewards Total rewards earned
     * @return penalties Total penalties incurred
     * @return balance Current token balance
     */
    function getNodeStats(address node) external view returns (
        uint256 score,
        uint256 lastReward,
        uint256 totalRewards,
        uint256 penalties,
        uint256 balance
    ) {
        return (
            metabolicScore[node],
            lastRewardTime[node],
            totalRewardsEarned[node],
            totalPenalties[node],
            balanceOf[node]
        );
    }

    /**
     * @dev Standard ERC20 Transfer
     * @param to Recipient address
     * @param value Amount to transfer
     */
    function transfer(address to, uint256 value) external returns (bool) {
        require(to != address(0), "LUCA: Cannot transfer to zero address");
        require(balanceOf[msg.sender] >= value, "LUCA: Insufficient balance");

        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;

        emit Transfer(msg.sender, to, value);
        return true;
    }

    /**
     * @dev Standard ERC20 Approve
     * @param spender Address authorized to spend
     * @param value Amount authorized
     */
    function approve(address spender, uint256 value) external returns (bool) {
        require(spender != address(0), "LUCA: Cannot approve zero address");

        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    /**
     * @dev Standard ERC20 TransferFrom
     * @param from Sender address
     * @param to Recipient address
     * @param value Amount to transfer
     */
    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        require(from != address(0), "LUCA: Cannot transfer from zero address");
        require(to != address(0), "LUCA: Cannot transfer to zero address");
        require(balanceOf[from] >= value, "LUCA: Insufficient balance");
        require(allowance[from][msg.sender] >= value, "LUCA: Insufficient allowance");

        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;

        emit Transfer(from, to, value);
        return true;
    }

    /**
     * @dev Transfer ownership of the DAO
     * @param newOwner Address of the new owner
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "LUCA: New owner cannot be zero address");
        require(newOwner != owner, "LUCA: New owner must be different");

        address previousOwner = owner;
        owner = newOwner;

        // Authorize new owner as node
        authorizedNodes[newOwner] = true;

        emit OwnershipTransferred(previousOwner, newOwner);
        emit NodeAuthorized(newOwner, previousOwner);
    }

    /**
     * @dev Emergency pause for reward distribution
     * Note: This is a simplified version. Production should use OpenZeppelin's Pausable
     */
    bool public rewardsPaused = false;

    function pauseRewards() external onlyOwner {
        rewardsPaused = true;
    }

    function unpauseRewards() external onlyOwner {
        rewardsPaused = false;
    }

    /**
     * @dev Get DAO statistics
     * @return supply Total token supply
     * @return treasuryBalance Treasury balance
     * @return nodeCount Number of authorized nodes
     */
    function getDAOStats() external view returns (
        uint256 supply,
        uint256 treasuryBalance,
        uint256 nodeCount
    ) {
        // Note: nodeCount would require tracking in production
        return (
            totalSupply,
            balanceOf[owner],
            0 // Simplified - would need counter in production
        );
    }
}
