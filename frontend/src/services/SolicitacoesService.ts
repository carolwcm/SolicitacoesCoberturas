// frontend/src/services/SolicitacoesService.ts

import api from './api';

export interface ItemSolicitacao {
  id?: number;
  codigo_material: number;
  nome_material: string;
  quantidade_solicitada: number;
  quantidade_autorizada?: number | null;
  status_item?: string;
}

export interface SolicitacaoCobertura {
  id?: number;
  prontuario: number;
  nome_paciente: string;
  leito?: string | null;
  solicitante: string;
  status?: string;
  auditor_username?: string | null;
  data_auditoria?: string | null;
  justificativa?: string | null;
  farmaceutico_username?: string | null;
  data_entrega?: string | null;
  created_at?: string;
  updated_at?: string;
  itens: ItemSolicitacao[];
}

export interface AuditoriaPayload {
  status_geral: string;
  justificativa: string;
  itens: {
    id: number;
    quantidade_autorizada: number | null;
    status_item: string;
  }[];
}

class SolicitacoesService {
  async listar(status?: string): Promise<SolicitacaoCobertura[]> {
    const params = status ? { status } : {};
    const response = await api.get('/api/solicitacoes', { params });
    return response.data;
  }

  async obterPorId(id: number): Promise<SolicitacaoCobertura> {
    const response = await api.get(`/api/solicitacoes/${id}`);
    return response.data;
  }

  async auditar(id: number, payload: AuditoriaPayload): Promise<SolicitacaoCobertura> {
    const response = await api.put(`/api/solicitacoes/${id}/auditar`, payload);
    return response.data;
  }

  async entregar(id: number): Promise<SolicitacaoCobertura> {
    const response = await api.put(`/api/solicitacoes/${id}/entregar`);
    return response.data;
  }

  async criarMock(solicitacao: SolicitacaoCobertura): Promise<SolicitacaoCobertura> {
    const response = await api.post('/api/solicitacoes', solicitacao);
    return response.data;
  }
}

export default new SolicitacoesService();
