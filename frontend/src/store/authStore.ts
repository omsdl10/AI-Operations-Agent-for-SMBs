import { create } from 'zustand';

import type { TokenPair, User } from '../types/auth';

type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  setAuth: (tokens: TokenPair, user: User) => void;
  logout: () => void;
};

const ACCESS_TOKEN_KEY = 'aiops_access_token';
const REFRESH_TOKEN_KEY = 'aiops_refresh_token';
const USER_KEY = 'aiops_user';

const getStoredUser = () => {
  const storedUser = localStorage.getItem(USER_KEY);
  return storedUser ? (JSON.parse(storedUser) as User) : null;
};

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: localStorage.getItem(ACCESS_TOKEN_KEY),
  refreshToken: localStorage.getItem(REFRESH_TOKEN_KEY),
  user: getStoredUser(),
  setAuth: (tokens, user) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    set({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token, user });
  },
  logout: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    set({ accessToken: null, refreshToken: null, user: null });
  },
}));

export const getAccessToken = () => useAuthStore.getState().accessToken;

