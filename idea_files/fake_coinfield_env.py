import gym
import coinfieldClient as cfc


class fakeCoinFieldEnv(gym.Env):
    cfClient = cfc.CoinfieldClient()

    wallet = {"btc": 0, "cad": 0, "eth": 0, "xrp": 0, "ltc": 0, "usd": 0, "eur": 0,
              "jpy": 0, "gbp": 0, "aed": 0, "dash": 0, "zec": 0, "btg": 0, "bch": 0,
              "zrx": 0, "gnt": 0, "rep": 0, "omg": 0, "salt": 0, "bat": 0, "zil": 0,
              "xlm": 0, "dgb": 0, "cvc": 0, "loom": 0, "c": 0}

    marketList = {"btccad", "ethcad", "ltccad", "btcusd", "ethusd", "xrpusd", "ltcusd", "btceur", "etheur",
                  "xrpeur", "ltceur", "xrpjpy", "xrpgbp", "xrpaed", "ethxrp", "btcxrp", "dashxrp", "ltcxrp", "zecxrp",
                  "btgxrp", "bchxrp", "zrxxrp", "gntxrp", "repxrp", "omgxrp", "saltxrp", "batxrp", "zilxrp",
                  "xlmusd", "xlmcad", "xlmeur", "xlmxrp", "dgbxrp", "cvcxrp", "loomxrp", "xrpusdc", "btcusdc", "xrpcad"}

    orderData = []

    feeData = []
    
    def __init__(self, arg1, arg2, ...):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input:
        self.observation_space = spaces.Box(low=0, high=255, shape=
                        (HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)

    def step(self, action):
        # Execute one time step within the environment
        ...
    def reset(self):
        # Reset the state of the environment to an initial state
        ...
    def render(self, mode='human', close=False):
        # Render the environment to the screen
        ...

    def __init__(self):
        pass

    def _step(self, action):
        """

        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self._take_action(action)
        self.status = self.env.step()
        reward = 0 #self._get_reward()
        ob = self.env.getState()
        episode_over = 0 # self.status != hfo_py.IN_GAME
        return ob, reward, episode_over, {}

    def _reset(self):
        pass

    def _fetchData(self):
        statusData = self.cfClient.GetStatus()["status"]
        if statusData == "ok":
            self.feeData = self.cfClient.GetFees()["fees"]
            for market in self.marketList:
                self.orderData[market] = self.cfClient.GetOrderbook(market)[market]
        else:
            print("SERVER UNAVAILABLE")

    def _take_action(self, action):
        for market in action:
            if market.action == "buy":
                self.wallet[market.crypt1] += (market.amount * self.orderData[market.name] - self.feeData[market.name].fee)
                self.wallet[market.crypt2] -= market.amount
            elif market.action == "sell":
                self.wallet[market.crypt2] += (market.amount * self.orderData[market.name] - self.feeData[market.name].fee)
                self.wallet[market.crypt1] -= market.amount
            elif market.action == "wait":
                pass

    def _get_reward(self):
        reward = 0
        for currency in self.wallet.keys():
            if (str(currency) + "cad") in self.marketList:
                # for
                reward += currency * self.orderData
            elif (str(currency) + "xrp") in self.marketList:
