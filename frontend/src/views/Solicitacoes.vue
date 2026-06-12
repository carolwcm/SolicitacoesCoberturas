<template>
  <div class="space-y-6">
    <!-- Header Area -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 tracking-tight">
          {{ isCciras ? 'Portal CCIRAS - Auditoria de Curativos' : 'Portal Farmácia - Liberação de Curativos' }}
        </h1>
        <p class="text-sm text-slate-500 mt-1">
          {{ isCciras ? 'Análise técnica, pareceres e autorização de coberturas especiais.' : 'Monitoramento de pareceres, controle de estoques e liberação final.' }}
        </p>
      </div>

      <div class="flex items-center gap-3">
        <!-- CCIRAS manual import -->
        <Button v-if="isCciras" @click="importarDadosAghu" variant="primary" :loading="importing">
          <template #icon>
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H18.25" />
            </svg>
          </template>
          Atualizar
        </Button>

        <!-- Farmácia manual update -->
        <Button v-else @click="atualizarParecerCciras" variant="primary" :loading="loading">
          <template #icon>
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H18.25" />
            </svg>
          </template>
          Atualizar Parecer CCIRAS
        </Button>

        <!-- AGHU Simulation to ease testing -->
        <Button @click="showSimuladorModal = true" variant="default">
          Simular AGHU
        </Button>

        <ProfileDropdown />
      </div>
    </div>

    <!-- Admin View Toggle Selector -->
    <div v-if="authStore.isAdmin" class="flex justify-center bg-white p-2.5 rounded-2xl shadow-sm border border-slate-100 max-w-md mx-auto">
      <div class="grid grid-cols-2 gap-2 w-full">
        <button 
          @click="modoExibicao = 'cciras'"
          :class="[
            modoExibicao === 'cciras' 
              ? 'bg-indigo-650 text-white shadow-sm' 
              : 'bg-transparent text-slate-650 hover:bg-slate-50',
            'py-2 px-4 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer text-center'
          ]"
        >
          Visual CCIRAS
        </button>
        <button 
          @click="modoExibicao = 'farmacia'"
          :class="[
            modoExibicao === 'farmacia' 
              ? 'bg-indigo-650 text-white shadow-sm' 
              : 'bg-transparent text-slate-650 hover:bg-slate-50',
            'py-2 px-4 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer text-center'
          ]"
        >
          Visual Farmácia
        </button>
      </div>
    </div>

    <!-- METRICS CARDS SECTION -->
    <!-- CCIRAS Metrics -->
    <div v-if="isCciras" class="grid grid-cols-2 md:grid-cols-6 gap-4">
      <div v-for="card in ccirasCards" :key="card.title" class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow duration-200">
        <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">{{ card.title }}</span>
        <span class="text-3xl font-extrabold mt-2" :class="card.color">{{ card.value }}</span>
      </div>
    </div>

    <!-- Farmácia Metrics -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="card in farmaciaCards" :key="card.title" class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow duration-200">
        <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">{{ card.title }}</span>
        <span class="text-3xl font-extrabold mt-2" :class="card.color">{{ card.value }}</span>
      </div>
    </div>

    <!-- TABLE SECTION -->
    <Card>
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-bold text-slate-700">Solicitações de Cobertura</h2>
          <span class="text-xs text-slate-400">Próxima sincronização automática em: {{ tempoParaSincronizar }} min</span>
        </div>
      </template>

      <div v-if="loading" class="py-12 flex justify-center">
        <LoadingIndicator />
      </div>
      <div v-else-if="solicitacoesFiltradas.length === 0" class="py-12 text-center text-slate-500 font-medium">
        Nenhuma solicitação encontrada no momento.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-100">
          <thead class="bg-slate-50">
            <!-- CCIRAS Headers -->
            <tr v-if="isCciras">
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Data</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Paciente</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Prontuário</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Unidade Solicitante</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Leito</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Itens Solicitados</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Situação</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Ações</th>
            </tr>
            <!-- Farmacia Headers -->
            <tr v-else>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Data</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Paciente</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Prontuário</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Unidade Solicitante</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Leito</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Situação CCIRAS</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-slate-100">
            <tr v-for="sol in solicitacoesFiltradas" :key="sol.id" class="hover:bg-slate-50/50 transition-colors duration-150">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-medium">{{ formatarData(sol.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800">{{ sol.nome_paciente }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.prontuario }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.leito ? 'Ala Curativos' : 'Unidade Geral' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-semibold">{{ sol.leito || 'N/A' }}</td>
              
              <!-- CCIRAS Item column -->
              <td v-if="isCciras" class="px-6 py-4 text-sm text-slate-600">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-55 text-indigo-700">
                  {{ sol.itens.length }} item(ns)
                </span>
              </td>

              <!-- Status column -->
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="getStatusBadgeClass(sol.status)">
                  {{ sol.status }}
                </span>
              </td>

              <!-- Actions column -->
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button @click="abrirAcoes(sol)" class="text-indigo-600 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 p-2 rounded-xl transition duration-150 inline-flex items-center cursor-pointer">
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <!-- DETALHES MODAL (CCIRAS & FARMÁCIA) -->
    <Modal :show="showDetalhesModal" @close="showDetalhesModal = false">
      <template #header>
        Detalhes da Solicitação #{{ solicitacaoSelecionada?.id }}
      </template>

      <div class="space-y-6 py-2" v-if="solicitacaoSelecionada">
        <!-- Cabeçalho de Informações do Paciente -->
        <div class="grid grid-cols-2 gap-4 text-sm bg-slate-50 p-4 rounded-2xl border border-slate-100">
          <div><span class="font-semibold text-slate-500">Paciente:</span> {{ solicitacaoSelecionada.nome_paciente }}</div>
          <div><span class="font-semibold text-slate-500">Prontuário:</span> {{ solicitacaoSelecionada.prontuario }}</div>
          <div><span class="font-semibold text-slate-500">Unidade Solicitante:</span> {{ solicitacaoSelecionada.leito ? 'Ala Curativos' : 'Unidade Geral' }}</div>
          <div><span class="font-semibold text-slate-500">Leito:</span> {{ solicitacaoSelecionada.leito || 'N/A' }}</div>
          <div><span class="font-semibold text-slate-500">Data e Hora:</span> {{ formatarData(solicitacaoSelecionada.created_at) }}</div>
          <div><span class="font-semibold text-slate-500">Solicitante:</span> {{ solicitacaoSelecionada.solicitante }}</div>
        </div>

        <!-- Parecer CCIRAS anterior (exibido para a Farmácia) -->
        <div v-if="!isCciras && solicitacaoSelecionada.auditor_username" class="border border-indigo-100 bg-indigo-50/20 rounded-2xl p-4 space-y-2">
          <h3 class="font-bold text-indigo-950 text-sm">Parecer Anterior da CCIRAS</h3>
          <div class="grid grid-cols-2 gap-2 text-xs text-indigo-900">
            <div><span class="font-medium">Auditor:</span> {{ solicitacaoSelecionada.auditor_username }}</div>
            <div><span class="font-medium">Data:</span> {{ formatarData(solicitacaoSelecionada.data_auditoria) }}</div>
          </div>
          <p class="text-sm text-indigo-950 mt-2 italic">"{{ solicitacaoSelecionada.justificativa }}"</p>
        </div>

        <!-- LISTA DE ITENS PARA EDICAO -->
        <div>
          <h3 class="font-bold text-slate-800 mb-3">Coberturas e Quantidades</h3>
          <div class="space-y-3">
            <div v-for="item in (isCciras ? itensEdicao : itensEdicao.filter(i => i.status_item === 'AUTORIZADO' || i.status_item === 'NEGADO'))" :key="item.id" class="border border-slate-150 rounded-2xl p-4 bg-white flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div class="flex-1">
                <p class="font-semibold text-slate-900">{{ item.nome_material }}</p>
                <p class="text-xs text-slate-500">Código: {{ item.codigo_material }}</p>
              </div>

              <!-- Controle de Qtd para CCIRAS -->
              <div v-if="isCciras" class="flex items-center gap-4">
                <div>
                  <span class="text-xs text-slate-400 block mb-1">Solicitada</span>
                  <span class="text-sm font-bold text-slate-800">{{ item.quantidade_solicitada }}</span>
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Autorizada</label>
                  <input type="number" v-model.number="item.quantidade_autorizada" min="0" :max="item.quantidade_solicitada" class="border rounded-xl p-1.5 w-24 text-center font-bold">
                </div>
              </div>

              <!-- Controle de Qtd para Farmácia -->
              <div v-else class="flex items-center gap-4">
                <div>
                  <span class="text-xs text-slate-400 block mb-1">Autorizada CCIRAS</span>
                  <span class="text-sm font-bold text-slate-800">{{ item.quantidade_autorizada }}</span>
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Liberada</label>
                  <input type="number" v-model.number="item.quantidade_liberada" min="0" :max="item.quantidade_autorizada" class="border rounded-xl p-1.5 w-24 text-center font-bold">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- PARECER TEXTAREA -->
        <div v-if="isCciras" class="form-group">
          <label class="block text-sm font-bold text-slate-700 mb-2">Parecer da CCIRAS</label>
          <textarea v-model="parecerCciras" rows="3" class="w-full border rounded-2xl p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Digite a análise técnica e justificativa..."></textarea>
        </div>

        <div v-else class="form-group">
          <label class="block text-sm font-bold text-slate-700 mb-2">Parecer da Farmácia</label>
          <textarea v-model="parecerFarmacia" rows="3" class="w-full border rounded-2xl p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Digite a justificativa de entrega/liberação..."></textarea>
        </div>
      </div>

      <!-- DECISION BUTTONS -->
      <template #footer>
        <div class="flex flex-wrap gap-2 justify-end w-full">
          <!-- CCIRAS Actions (4 buttons) -->
          <template v-if="isCciras">
            <Button @click="submeterDecisaoCciras('EM ANÁLISE')" variant="default">Em Análise</Button>
            <Button @click="submeterDecisaoCciras('NEGADO')" variant="danger">Negar</Button>
            <Button @click="submeterDecisaoCciras('AUTORIZADO')" variant="primary">Autorizar</Button>
            <Button @click="submeterDecisaoCciras('LIBERADO')" variant="success">Liberar</Button>
          </template>

          <!-- Farmácia Actions (2 buttons) -->
          <template v-else>
            <Button @click="submeterDecisaoFarmacia('EM FALTA')" variant="danger">Em Falta</Button>
            <Button @click="submeterDecisaoFarmacia('LIBERADO')" variant="success">Liberar</Button>
          </template>
        </div>
      </template>
    </Modal>

    <!-- SIMULADOR AGHU MODAL -->
    <Modal :show="showSimuladorModal" @close="showSimuladorModal = false">
      <template #header>Simulador de Entrada AGHU</template>
      <div class="space-y-4 py-2">
        <p class="text-sm text-slate-500">
          Simule o fluxo de um profissional solicitando coberturas especiais de curativos no sistema AGHU do hospital.
        </p>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Paciente</label>
          <input type="text" v-model="simuladoPaciente" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Nome Completo do Paciente">
        </div>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Prontuário (Apenas números)</label>
          <input type="number" v-model.number="simuladoProntuario" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Ex: 87462">
        </div>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Leito</label>
          <input type="text" v-model="simuladoLeito" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Ex: Leito 12 - UTI">
        </div>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Solicitante</label>
          <input type="text" v-model="simuladoSolicitante" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Ex: Enf. Mariana Souza">
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-2">Itens de Coberturas para Curativos</label>
          <div class="space-y-2 max-h-48 overflow-y-auto border rounded-xl p-3 bg-slate-50">
            <div v-for="item in coberturasPredefinidas" :key="item.codigo" class="flex items-center justify-between">
              <label class="flex items-center text-sm text-slate-700 cursor-pointer">
                <input type="checkbox" :value="item" v-model="simuladoItensSelecionados" class="rounded border-slate-300 text-indigo-600">
                <span class="ml-2 text-xs font-medium">{{ item.nome }}</span>
              </label>
              <div v-if="simuladoItensSelecionados.some(i => i.codigo === item.codigo)" class="flex items-center gap-2">
                <span class="text-xs text-slate-400">Qtd:</span>
                <input type="number" v-model.number="item.qtd" min="1" class="border rounded px-1.5 py-0.5 w-12 text-center text-xs">
              </div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button @click="showSimuladorModal = false" variant="default">Cancelar</Button>
        <Button @click="enviarSimulacaoAghu" variant="primary">Criar Solicitação</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useToast } from 'vue-toastification';
import SolicitacoesService, { SolicitacaoCobertura } from '../services/SolicitacoesService';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import LoadingIndicator from '../components/LoadingIndicator.vue';
import ProfileDropdown from '../components/ProfileDropdown.vue';
import { useAuthStore } from '../stores/auth';

const toast = useToast();
const authStore = useAuthStore();

// Perfil e Modo de Exibição
const modoExibicao = ref<'cciras' | 'farmacia'>('cciras');

const isCciras = computed(() => {
  if (authStore.isAdmin) {
    return modoExibicao.value === 'cciras';
  }
  return authStore.isCciras;
});

const loading = ref(false);
const importing = ref(false);
const solicitacoes = ref<SolicitacaoCobertura[]>([]);

// Modais
const showDetalhesModal = ref(false);
const showSimuladorModal = ref(false);
const solicitacaoSelecionada = ref<SolicitacaoCobertura | null>(null);

// Inputs para pareces e edições
const parecerCciras = ref('');
const parecerFarmacia = ref('');
const itensEdicao = ref<any[]>([]);

// Temporizadores para Sincronização Horária
const tempoParaSincronizar = ref(60);
let timerSincronizacao: any = null;

// Sincronização automática de hora em hora
const inicializarSincronizador = () => {
  timerSincronizacao = setInterval(() => {
    tempoParaSincronizar.value--;
    if (tempoParaSincronizar.value <= 0) {
      if (isCciras.value) {
        importarDadosAghu();
      } else {
        atualizarParecerCciras();
      }
      tempoParaSincronizar.value = 60;
    }
  }, 60000); // Executa a cada minuto
};

// Métricas Dinâmicas
const totalSolicitacoes = computed(() => solicitacoes.value.length);
const pendentesCount = computed(() => solicitacoes.value.filter(s => s.status === 'PENDENTE').length);
const emAnaliseCount = computed(() => solicitacoes.value.filter(s => s.status === 'EM ANÁLISE').length);
const autorizadasCount = computed(() => solicitacoes.value.filter(s => s.status === 'AUTORIZADO').length);
const negadasCount = computed(() => solicitacoes.value.filter(s => s.status === 'NEGADO').length);
const liberadasCount = computed(() => solicitacoes.value.filter(s => s.status === 'LIBERADO' || s.status === 'ENTREGUE').length);
const aguardandoLibCount = computed(() => solicitacoes.value.filter(s => s.status === 'AUTORIZADO' || s.status === 'PENDENTE').length);

const ccirasCards = computed(() => [
  { title: 'Total', value: totalSolicitacoes.value, color: 'text-slate-800' },
  { title: 'Pendentes', value: pendentesCount.value, color: 'text-yellow-600' },
  { title: 'Em análise', value: emAnaliseCount.value, color: 'text-orange-500' },
  { title: 'Autorizadas', value: autorizadasCount.value, color: 'text-blue-600' },
  { title: 'Negadas', value: negadasCount.value, color: 'text-rose-600' },
  { title: 'Liberadas', value: liberadasCount.value, color: 'text-emerald-600' }
]);

const farmaciaCards = computed(() => [
  { title: 'Aguardando Liberação', value: aguardandoLibCount.value, color: 'text-yellow-600' },
  { title: 'Negadas', value: negadasCount.value, color: 'text-rose-600' },
  { title: 'Liberadas', value: liberadasCount.value, color: 'text-emerald-600' },
  { title: 'Em análise', value: emAnaliseCount.value, color: 'text-orange-500' }
]);

const solicitacoesFiltradas = computed(() => {
  if (isCciras.value) {
    return solicitacoes.value;
  } else {
    // Farmácia visualiza apenas autorizadas, pendentes ou em análise que necessitam liberação
    return solicitacoes.value;
  }
});

const formatarData = (dataStr?: string | null) => {
  if (!dataStr) return 'N/A';
  return new Date(dataStr).toLocaleString('pt-BR');
};

const getStatusBadgeClass = (status?: string) => {
  switch (status?.toUpperCase()) {
    case 'PENDENTE':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-yellow-50 text-yellow-700 border border-yellow-200';
    case 'EM ANÁLISE':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-orange-50 text-orange-700 border border-orange-200';
    case 'AUTORIZADO':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200';
    case 'NEGADO':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200';
    case 'LIBERADO':
    case 'ENTREGUE':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
    case 'EM FALTA':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-700 border border-slate-350';
    default:
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-50 text-slate-600';
  }
};

const carregarSolicitacoes = async () => {
  loading.value = true;
  try {
    solicitacoes.value = await SolicitacoesService.listar();
  } catch (err) {
    toast.error('Falha ao carregar as solicitações.');
  } finally {
    loading.value = false;
  }
};

const importarDadosAghu = async () => {
  importing.value = true;
  try {
    await api.post('/api/solicitacoes/importar');
    toast.success('Dados importados com sucesso do AGHU!');
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Erro ao conectar e importar dados do AGHU.');
  } finally {
    importing.value = false;
  }
};

const atualizarParecerCciras = async () => {
  await carregarSolicitacoes();
  toast.success('Pareceres da CCIRAS atualizados!');
};

// Ações ao clicar na tabela
const abrirAcoes = (sol: SolicitacaoCobertura) => {
  solicitacaoSelecionada.value = sol;
  parecerCciras.value = sol.justificativa || '';
  parecerFarmacia.value = sol.parecer_farmacia || '';
  itensEdicao.value = sol.itens.map(i => ({
    ...i,
    quantidade_autorizada: i.quantidade_autorizada !== null && i.quantidade_autorizada !== undefined ? i.quantidade_autorizada : i.quantidade_solicitada,
    quantidade_liberada: i.quantidade_liberada !== null && i.quantidade_liberada !== undefined ? i.quantidade_liberada : (i.quantidade_autorizada || i.quantidade_solicitada)
  }));
  showDetalhesModal.value = true;
};

// CCIRAS Decision Submission
const submeterDecisaoCciras = async (statusGeral: string) => {
  if (!solicitacaoSelecionada.value?.id) return;
  if (!parecerCciras.value.trim()) {
    toast.warning('Por favor, registre a justificativa técnica/parecer da CCIRAS.');
    return;
  }

  try {
    const payload = {
      status_geral: statusGeral,
      justificativa: parecerCciras.value,
      itens: itensEdicao.value.map(i => ({
        id: i.id!,
        quantidade_autorizada: i.quantidade_autorizada,
        status_item: statusGeral === 'NEGADO' ? 'NEGADO' : 'AUTORIZADO'
      }))
    };
    await SolicitacoesService.auditar(solicitacaoSelecionada.value.id, payload);
    toast.success('Parecer da CCIRAS enviado com sucesso!');
    showDetalhesModal.value = false;
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Falha ao registrar a auditoria da CCIRAS.');
  }
};

// Farmácia Decision Submission
const submeterDecisaoFarmacia = async (statusGeral: string) => {
  if (!solicitacaoSelecionada.value?.id) return;
  if (!parecerFarmacia.value.trim()) {
    toast.warning('Por favor, registre a justificativa/parecer da Farmácia.');
    return;
  }

  try {
    const payload = {
      status_geral: statusGeral,
      justificativa: parecerFarmacia.value,
      itens: itensEdicao.value.map(i => ({
        id: i.id!,
        quantidade_liberada: i.quantidade_liberada
      }))
    };
    await SolicitacoesService.entregar(solicitacaoSelecionada.value.id, payload);
    toast.success('Decisão da Farmácia registrada!');
    showDetalhesModal.value = false;
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Falha ao registrar a liberação da Farmácia.');
  }
};

// AGHU SIMULATION FIELDS
const simuladoPaciente = ref('Ana Maria Custódio');
const simuladoProntuario = ref(384729);
const simuladoLeito = ref('Leito 104 - Enfermaria');
const simuladoSolicitante = ref('Dr. Juliano Bastos');
const simuladoItensSelecionados = ref<any[]>([]);

const coberturasPredefinidas = ref([
  { codigo: 10401, nome: 'Curativo Hidrocolóide Extra Fino 10x10', qtd: 5 },
  { codigo: 10402, nome: 'Curativo com Prata Nanocristalina 10x12', qtd: 2 },
  { codigo: 10403, nome: 'Espuma de Poliuretano com Silicone', qtd: 4 },
  { codigo: 10404, nome: 'Alginato de Cálcio e Sódio', qtd: 3 }
]);

const enviarSimulacaoAghu = async () => {
  if (!simuladoPaciente.value || !simuladoProntuario.value || simuladoItensSelecionados.value.length === 0) {
    toast.warning('Preencha os campos obrigatórios e escolha coberturas.');
    return;
  }

  try {
    const payload: SolicitacaoCobertura = {
      prontuario: simuladoProntuario.value,
      nome_paciente: simuladoPaciente.value,
      leito: simuladoLeito.value,
      solicitante: simuladoSolicitante.value,
      itens: simuladoItensSelecionados.value.map(i => ({
        codigo_material: i.codigo,
        nome_material: i.nome,
        quantidade_solicitada: i.qtd
      }))
    };
    await SolicitacoesService.criarMock(payload);
    toast.success('Solicitação simulada criada!');
    showSimuladorModal.value = false;
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Erro ao simular solicitação.');
  }
};

onMounted(() => {
  carregarSolicitacoes();
  inicializarSincronizador();
  
  // Define o modo inicial
  if (authStore.isAdmin) {
    modoExibicao.value = 'cciras';
  } else if (authStore.isCciras) {
    modoExibicao.value = 'cciras';
  } else if (authStore.isFarmacia) {
    modoExibicao.value = 'farmacia';
  }
});

onUnmounted(() => {
  if (timerSincronizacao) {
    clearInterval(timerSincronizacao);
  }
});
</script>
