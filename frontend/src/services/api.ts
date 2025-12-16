import axios from 'axios';
import type {
    Member,
    Claim,
    Decision,
    Document,
    ClaimSubmitResponse,
    ClaimFilters
} from '../types';

/* ===========================
   AXIOS INSTANCE
=========================== */

const api = axios.create({
    baseURL: 'https://jarrod-pseudomorular-caitlin.ngrok-free.dev',
    headers: {
        'Content-Type': 'application/json',
    },
});

/* ===========================
   HELPERS
=========================== */

const normalizeArray = <T>(data: any, label: string): T[] => {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data?.data)) return data.data;
    if (Array.isArray(data?.items)) return data.items;

    console.error(`Unexpected ${label} response shape:`, data);
    return [];
};

/* ===========================
   MEMBERS
=========================== */

export const fetchMembers = async (): Promise<Member[]> => {
    try {
        const response = await api.get('/members');
        return normalizeArray<Member>(response.data, 'members');
    } catch (error) {
        console.error('Error fetching members:', error);
        return [];
    }
};

export const getMember = async (memberId: string): Promise<Member | null> => {
    try {
        const response = await api.get(`/members/${memberId}`);
        return response.data ?? null;
    } catch (error) {
        console.error(`Error fetching member ${memberId}:`, error);
        return null;
    }
};

/* ===========================
   CLAIMS
=========================== */

export const submitClaim = async (
    formData: FormData
): Promise<ClaimSubmitResponse> => {
    const response = await api.post<ClaimSubmitResponse>(
        '/claims',
        formData,
        {
            headers: { 'Content-Type': 'multipart/form-data' },
        }
    );
    return response.data;
};

export const getClaim = async (claimId: string): Promise<Claim | null> => {
    try {
        const response = await api.get(`/claims/${claimId}`);
        return response.data ?? null;
    } catch (error) {
        console.error(`Error fetching claim ${claimId}:`, error);
        return null;
    }
};

export const listClaims = async (
    filters?: ClaimFilters
): Promise<Claim[]> => {
    try {
        const response = await api.get('/claims', { params: filters });
        return normalizeArray<Claim>(response.data, 'claims');
    } catch (error) {
        console.error('Error listing claims:', error);
        return [];
    }
};

/* ===========================
   DOCUMENTS
=========================== */

export const getClaimDocuments = async (
    claimId: string
): Promise<Document[]> => {
    try {
        const response = await api.get(`/claims/${claimId}/documents`);
        return normalizeArray<Document>(response.data, 'documents');
    } catch (error) {
        console.error(`Error fetching documents for claim ${claimId}:`, error);
        return [];
    }
};

/* ===========================
   DECISIONS
=========================== */

export const getDecision = async (
    claimId: string
): Promise<Decision | null> => {
    try {
        const response = await api.get(`/decisions/${claimId}`);
        return response.data ?? null;
    } catch (error) {
        console.error(`Error fetching decision for claim ${claimId}:`, error);
        return null;
    }
};

export default api;
