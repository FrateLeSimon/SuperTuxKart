import gym
import numpy as np
import pystk

class SimplePyTux(gym.Env):
    """
    Wrapper Gym minimaliste pour SuperTuxKart.
    Observation :
        - image (128x96x3)
        - velocity (3,)
        - rotation (4,)
    Action :
        - steer [-1,1], acc [0,1], brake [0,1], drift [0,1]
    """
    def __init__(self, track='lighthouse', width=128, height=96, max_length=1000):
        super().__init__()
        self.track = track
        self.width = width
        self.height = height
        self.max_length = max_length
        self.t = 0
        self._rescue_timer = 30
        self._last_rescue = 0
        self._init_pystk()
        self.observation_space = gym.spaces.Dict({
            'image': gym.spaces.Box(0, 255, (height, width, 3), dtype=np.uint8),
            'velocity': gym.spaces.Box(-np.inf, np.inf, (3,), dtype=np.float32),
            'rotation': gym.spaces.Box(-1, 1, (4,), dtype=np.float32)
        })
        self.action_space = gym.spaces.Box(
            low=np.array([-1, 0, 0, 0]),
            high=np.array([1, 1, 1, 1]),
            dtype=np.float32
        )

    def _init_pystk(self):
        config = pystk.GraphicsConfig.hd()
        config.screen_width = self.width
        config.screen_height = self.height
        pystk.init(config)
        self.race = None

    def reset(self):
        if self.race is not None:
            self.race.stop()
            del self.race
        race_cfg = pystk.RaceConfig(
            num_kart=1, laps=1, track=self.track, difficulty=0
        )
        race_cfg.players[0].controller = pystk.PlayerConfig.Controller.PLAYER_CONTROL
        self.race = pystk.Race(race_cfg)
        self.race.start()
        self.t = 0
        self._last_rescue = 0
        self.max_distance = 0
        self._state = pystk.WorldState()
        self._track = pystk.Track()
        self.race.step()
        return self._get_obs()

    def _get_obs(self):
        self._state.update()
        self._track.update()
        image = np.array(self.race.render_data[0].image)
        kart = self._state.players[0].kart
        velocity = np.asarray(kart.velocity, dtype=np.float32)
        rotation = np.asarray(kart.rotation, dtype=np.float32)
        return {
            'image': image,
            'velocity': velocity,
            'rotation': rotation
        }

    def step(self, action):
        self.t += 1
        # Action : [steer, acc, brake, drift]
        steer, acc, brake, drift = action
        a = pystk.Action()
        a.steer = float(steer)
        a.acceleration = float(acc)
        a.brake = float(brake)
        a.drift = float(drift) > 0.5
        obs = self._get_obs()
        kart = self._state.players[0].kart
        # Rescue automatique si bloqué
        if np.linalg.norm(obs['velocity']) < 1.0 and (self.t - self._last_rescue) > self._rescue_timer:
            self._last_rescue = self.t
            a.rescue = True
        self.race.step(a)
        reward = self._calc_reward(kart)
        done = self.t >= self.max_length or kart.overall_distance >= self._track.length
        return self._get_obs(), reward, done, {}

    def _calc_reward(self, kart):
        # Reward = distance parcourue depuis le dernier step
        r = 0
        if hasattr(self, 'max_distance'):
            if kart.overall_distance > self.max_distance:
                r = kart.overall_distance - self.max_distance
                self.max_distance = kart.overall_distance
        else:
            self.max_distance = kart.overall_distance
        return r

    def render(self, mode='human'):
        # Optionnel : afficher l'image avec matplotlib
        import matplotlib.pyplot as plt
        obs = self._get_obs()
        plt.imshow(obs['image'])
        plt.title(f"Step {self.t}")
        plt.pause(0.01)

    def close(self):
        if self.race is not None:
            self.race.stop()
            del self.race
        pystk.clean() 