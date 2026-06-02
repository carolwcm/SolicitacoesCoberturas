<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Solicitações de Cobertura</h1>
      <Button @click="sincronizarAGHU" :disabled="sincronizando" variant="primary" class="flex items-center space-x-2">
        <svg v-if="sincronizando" class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ sincronizando ? 'Sincronizando...' : 'Sincronizar AGHU' }}</span>
      </Button>
    </div>

    <!-- Filtros de Status -->
    <Card class="mb-6">
      <div class="flex flex-wrap gap-2">
        <Button 
          v-for="statusFilter in ['TODAS', 'PENDENTE', 'AUTORIZADO', 'NEGADO', 'ENTREGUE']" 
          :key="statusFilter"
          @click="filtroStatus = statusFilter"
          :variant="filtroStatus === statusFilter ? 'primary' : 'default'"
          size="sm"
        >
          {{ statusFilter }}
        </Button>
      </div>
    </Card>

    <!-- Tabela de Solicitações -->
    <Card>
      <div class="w-full overflow-x-auto rounded-lg">
        <table class="w-full whitespace-no-wrap">
          <thead>
            <tr class="text-xs font-semibold tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50">
              <th class="px-4 py-3">ID</th>
              <th class="px-4 py-3">Prontuário</th>
              <th class="px-4 py-3">Paciente</th>
              <th class="px-4 py-3">Leito</th>
              <th class="px-4 py-3">Solicitante</th>
              <th class="px-4 py-3">Status</th>
              <th class="px-4 py-3 text-right">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-100">
            <tr v-for="sol in solicitacoesFiltradas" :key="sol.id" class="text-gray-700 hover:bg-gray-50/50 transition-colors">
              <td class="px-4 py-3 text-sm font-semibold">#{{ sol.id }}</td>
              <td class="px-4 py-3 text-sm">{{ sol.prontuario }}</td>
              <td class="px-4 py-3 text-sm font-medium">{{ sol.nome_paciente }}</td>
              <td class="px-4 py-3 text-sm text-gray-500">{{ sol.leito || 'N/I' }}</td>
              <td class="px-4 py-3 text-sm text-gray-500">{{ sol.solicitante }}</td>
              <td class="px-4 py-3 text-xs">
                <span :class="getStatusBadgeClass(sol.status)" class="px-2.5 py-1 rounded-full font-semibold">
                  {{ sol.status }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-right space-x-2">
                <!-- Ações para a CCIRAS (Auditar) -->
                <Button 
                  v-if="podeAuditar(sol.status)" 
                  @click="abrirAuditoria(sol)" 
                  variant="success" 
                  size="sm"
                >
                  Auditar
                </Button>

                <!-- Ações para a Farmácia (Entregar) -->
                <Button 
                  v-if="podeEntregar(sol.status)" 
                  @click="entregarSolicitacao(sol)" 
                  variant="warning" 
                  size="sm"
                  :disabled="entregandoId === sol.id"
                >
                  {{ entregandoId === sol.id ? 'Entregando...' : 'Entregar' }}
                </Button>

                <!-- Detalhes / Visualizar -->
                <Button @click="verDetalhes(sol)" variant="default" size="sm">
                  Ver Detalhes
                </Button>
              </td>
            </tr>
            <tr v-if="solicitacoesFiltradas.length === 0">
              <td colspan="7" class="px-6 py-12 text-center text-gray-400">
                Nenhuma solicitação encontrada.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <!-- Modal de Auditoria (CCIRAS) -->
    <Modal :show="showModalAuditoria" @close="showModalAuditoria = false">
      <template #header>
        Auditar Solicitação #{{ solSelecionada?.id }}
      </template>

      <div class="space-y-4" v-if="solSelecionada">
        <div class="bg-gray-50 p-3 rounded-lg text-sm space-y-1">
          <p><strong>Paciente:</strong> {{ solSelecionada.nome_paciente }}</p>
          <p><strong>Prontuário:</strong> {{ solSelecionada.prontuario }} | <strong>Leito:</strong> {{ solSelecionada.leito || 'N/I' }}</p>
          <p><strong>Solicitado por:</strong> {{ solSelecionada.solicitante }}</p>
        </div>

        <h3 class="font-bold text-gray-700 text-sm border-b pb-2">Itens para Auditoria</h3>
        <div class="space-y-3">
          <div v-for="item in itensParaAuditoria" :key="item.id" class="border p-3 rounded-lg space-y-2 bg-white">
            <div class="flex justify-between items-center">
              <span class="font-semibold text-sm">{{ item.nome_material }}</span>
              <span class="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">Qtd Solicitada: {{ item.quantidade_solicitada }}</span>
            </div>
            
            <div class="grid grid-cols-2 gap-4 pt-1">
              <div>
                <label class="block text-xs font-semibold text-gray-500 mb-1">Decisão do Item</label>
                <select v-model="item.status_item" class="form-control text-sm">
                  <option value="PENDENTE">PENDENTE</option>
                  <option value="AUTORIZADO">AUTORIZAR</option>
                  <option value="NEGADO">NEGAR</option>
                </select>
              </div>
              <div v-if="item.status_item === 'AUTORIZADO'">
                <label class="block text-xs font-semibold text-gray-500 mb-1">Qtd Autorizada</label>
                <input 
                  type="number" 
                  v-model.number="item.quantidade_autorizada" 
                  :max="item.quantidade_solicitada" 
                  min="0"
                  class="form-control text-sm"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Justificativa CCIRAS -->
        <div>
          <label class="block text-xs font-semibold text-gray-600 mb-1">Justificativa da Decisão (Obrigatório)</label>
          <textarea v-model="justificativaAuditoria" rows="3" placeholder="Insira a justificativa clínica..." class="form-control text-sm"></textarea>
        </div>
      </div>

      <template #footer>
        <Button @click="showModalAuditoria = false" variant="default">Cancelar</Button>
        <Button @click="salvarAuditoria" variant="primary" :disabled="salvandoAuditoria || !justificativaAuditoria.trim()">
          {{ salvandoAuditoria ? 'Salvando...' : 'Finalizar Auditoria' }}
        </Button>
      </template>
    </Modal>

    <!-- Modal de Detalhes (Visualização) -->
    <Modal :show="showModalDetalhes" @close="showModalDetalhes = false">
      <template #header>
        Detalhes da Solicitação #{{ solSelecionada?.id }}
      </template>

      <div class="space-y-4 text-sm" v-if="solSelecionada">
        <div class="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl">
          <div><span class="text-gray-500">Prontuário:</span> <p class="font-semibold">{{ solSelecionada.prontuario }}</p></div>
          <div><span class="text-gray-500">Paciente:</span> <p class="font-semibold">{{ solSelecionada.nome_paciente }}</p></div>
          <div><span class="text-gray-500">Leito:</span> <p class="font-semibold">{{ solSelecionada.leito || 'N/I' }}</p></div>
          <div><span class="text-gray-500">Status Geral:</span> 
            <p><span :class="getStatusBadgeClass(solSelecionada.status)" class="px-2.5 py-0.5 rounded-full text-xs font-semibold">{{ solSelecionada.status }}</span></p>
          </div>
        </div>

        <!-- Itens -->
        <div>
          <h3 class="font-bold text-gray-700 mb-2">Materiais Solicitados</h3>
          <div class="border rounded-lg divide-y bg-white">
            <div v-for="item in solSelecionada.itens" :key="item.id" class="p-3 flex justify-between items-center">
              <div>
                <p class="font-medium">{{ item.nome_material }}</p>
                <p class="text-xs text-gray-500">Cod. Material: {{ item.codigo_material }}</p>
              </div>
              <div class="text-right">
                <span class="text-xs font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700">Solicitado: {{ item.quantidade_solicitada }}</span>
                <div v-if="item.quantidade_autorizada !== null" class="mt-1">
                  <span class="text-xs font-semibold px-2 py-0.5 rounded" :class="item.status_item === 'AUTORIZADO' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
                    Autorizado: {{ item.quantidade_autorizada }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Dados de Auditoria se houver -->
        <div v-if="solSelecionada.data_auditoria" class="bg-indigo-50/50 border border-indigo-100 p-4 rounded-xl space-y-1">
          <h4 class="font-bold text-indigo-900 text-xs uppercase tracking-wider mb-2">Auditoria (CCIRAS)</h4>
          <p><span class="text-gray-500">Auditor:</span> {{ solSelecionada.auditor_username }}</p>
          <p><span class="text-gray-500">Data:</span> {{ formatarData(solSelecionada.data_auditoria) }}</p>
          <p><span class="text-gray-500">Justificativa:</span> {{ solSelecionada.justificativa }}</p>
        </div>

        <!-- Dados de Entrega se houver -->
        <div v-if="solSelecionada.data_entrega" class="bg-emerald-50/50 border border-emerald-100 p-4 rounded-xl space-y-1">
          <h4 class="font-bold text-emerald-900 text-xs uppercase tracking-wider mb-2">Entrega / Dispensação</h4>
          <p><span class="text-gray-500">Responsável:</span> {{ solSelecionada.farmaceutico_username }}</p>
          <p><span class="text-gray-500">Data de Entrega:</span> {{ formatarData(solSelecionada.data_entrega) }}</p>
        </div>
      </div>

      <template #footer>
        <Button @click="showModalDetalhes = false" variant="primary">Fechar</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';

const toast = useToast();
const authStore = useAuthStore();

const solicitacoes = ref<any[]>([]);
const sincronizando = ref(false);
const filtroStatus = ref('TODAS');

// Controle de Modais e Seleções
const showModalAuditoria = ref(false);
const showModalDetalhes = ref(false);
const solSelecionada = ref<any | null>(null);

// Auditoria Campos
const itensParaAuditoria = ref<any[]>([]);
const justificativaAuditoria = ref('');
const salvandoAuditoria = ref(false);

// Estado de Entrega
const entregandoId = ref<number | null>(null);

// Regras de Visualização baseado nos grupos do AD
const CCIRAS_GROUP = 'SOL-COB-CCIRAS';
const FARMACIA_GROUP = 'SOL-COB-FARMACIA';

const isCCIRAS = computed(() => {
  return authStore.user?.groups?.includes(CCIRAS_GROUP) || authStore.isAdmin;
});

const isFarmacia = computed(() => {
  return authStore.user?.groups?.includes(FARMACIA_GROUP) || authStore.isAdmin;
});

const podeAuditar = (status: string) => {
  return isCCIRAS.value && status === 'PENDENTE';
};

const podeEntregar = (status: string) => {
  return isFarmacia.value && status === 'AUTORIZADO';
};

const solicitacoesFiltradas = computed(() => {
  if (filtroStatus.value === 'TODAS') return solicitacoes.value;
  return solicitacoes.value.filter(s => s.status === filtroStatus.value);
});

const carregarSolicitacoes = async () => {
  try {
    const { data } = await api.get('/api/solicitacoes');
    solicitacoes.value = data;
  } catch (error) {
    toast.error('Erro ao carregar lista de solicitações.');
  }
};

const sincronizarAGHU = async () => {
  sincronizando.value = true;
  try {
    const { data } = await api.post('/api/solicitacoes/importar');
    toast.success(data.message || 'Sincronização concluída com sucesso.');
    await carregarSolicitacoes();
  } catch (error) {
    toast.error('Erro ao sincronizar com o AGHU.');
  } finally {
    sincronizando.value = false;
  }
};

const abrirAuditoria = (sol: any) => {
  solSelecionada.value = sol;
  justificativaAuditoria.value = '';
  // Clona os itens para edição no modal
  itensParaAuditoria.value = sol.itens.map((item: any) => ({
    id: item.id,
    nome_material: item.nome_material,
    quantidade_solicitada: item.quantidade_solicitada,
    quantidade_autorizada: item.quantidade_solicitada, // Valor inicial sugerido
    status_item: 'AUTORIZADO' // Sugere autorizar por padrão
  }));
  showModalAuditoria.value = true;
};

const salvarAuditoria = async () => {
  if (!solSelecionada.value) return;
  salvandoAuditoria.value = true;

  try {
    // Determina o status geral baseado na decisão dos itens
    const todosNegados = itensParaAuditoria.value.every(i => i.status_item === 'NEGADO');
    const statusGeral = todosNegados ? 'NEGADO' : 'AUTORIZADO';

    const payload = {
      status_geral: statusGeral,
      justificativa: justificativaAuditoria.value,
      itens: itensParaAuditoria.value.map(i => ({
        id: i.id,
        status_item: i.status_item,
        quantidade_autorizada: i.status_item === 'AUTORIZADO' ? i.quantidade_autorizada : 0
      }))
    };

    await api.put(`/api/solicitacoes/${solSelecionada.value.id}/auditar`, payload);
    toast.success('Auditoria realizada com sucesso!');
    showModalAuditoria.value = false;
    await carregarSolicitacoes();
  } catch (error: any) {
    const msg = error.response?.data?.detail || 'Erro ao salvar auditoria.';
    toast.error(msg);
  } finally {
    salvandoAuditoria.value = false;
  }
};

const entregarSolicitacao = async (sol: any) => {
  entregandoId.value = sol.id;
  try {
    await api.put(`/api/solicitacoes/${sol.id}/entregar`);
    toast.success(`Solicitação #${sol.id} entregue com sucesso!`);
    await carregarSolicitacoes();
  } catch (error) {
    toast.error('Erro ao registrar entrega da solicitação.');
  } finally {
    entregandoId.value = null;
  }
};

const verDetalhes = (sol: any) => {
  solSelecionada.value = sol;
  showModalDetalhes.value = true;
};

const getStatusBadgeClass = (status: string) => {
  switch (status) {
    case 'PENDENTE': return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
    case 'AUTORIZADO': return 'bg-green-100 text-green-800 border border-green-200';
    case 'NEGADO': return 'bg-red-100 text-red-800 border border-red-200';
    case 'ENTREGUE': return 'bg-blue-100 text-blue-800 border border-blue-200';
    default: return 'bg-gray-100 text-gray-800';
  }
};

const formatarData = (dataStr: string) => {
  if (!dataStr) return '';
  try {
    const d = new Date(dataStr);
    return d.toLocaleString('pt-BR');
  } catch (e) {
    return dataStr;
  }
};

onMounted(() => {
  carregarSolicitacoes();
});
</script>
