export type Business = {
  id: string;
  name: string;
};

export type User = {
  id: string;
  business_id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
  business?: Business | null;
};

export type TokenPair = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

export type AuthResponse = {
  tokens: TokenPair;
  user: User;
};

