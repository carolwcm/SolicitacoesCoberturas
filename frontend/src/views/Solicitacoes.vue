<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-slate-800">Solicitações de Cobertura Especial para Curativos</h1>
      
      <!-- Simulação de Recebimento do AGHU -->
      <Button @click="showSimuladorModal = true" variant="primary">
        <template #icon>
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </template>
        Simular Solicitação (AGHU)
      </Button>
    </div>

    <!-- Navegação por Abas -->
    <div class="border-b border-slate-200">
      <nav class="-mb-px flex space-x-8" aria-label="Tabs">
        <button
          v-for="tab in abas"
          :key="tab.id"
          @click="abaAtiva = tab.id"
          :class="[
            abaAtiva === tab.id
              ? 'border-indigo-500 text-indigo-600'
              : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300',
            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 cursor-pointer'
          ]"
        >
          {{ tab.nome }}
          <span
            v-if="tab.badge"
            class="ml-2 py-0.5 px-2.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800"
          >
            {{ tab.badge }}
          </span>
        </button>
      </nav>
    </div>

    <!-- Conteúdo da Aba CCIRAS -->
    <div v-if="abaAtiva === 'cciras'" class="space-y-4">
      <Card>
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-semibold text-slate-700">Painel de Auditoria - CCIRAS</h2>
            <span class="text-xs text-slate-500">Apenas membros com perfil de auditor (SOL-COB-CCIRAS) podem auditar</span>
          </div>
        </template>
        
        <div v-if="loading" class="py-12 flex justify-center">
          <LoadingIndicator />
        </div>
        <div v-else-if="solicitacoesPendentes.length === 0" class="py-12 text-center text-slate-500">
          Nenhuma solicitação aguardando auditoria.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Prontuário</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Paciente</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Leito</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Solicitante</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Itens</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-200">
              <tr v-for="sol in solicitacoesPendentes" :key="sol.id" class="hover:bg-slate-50 transition-colors duration-150">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-900">{{ sol.prontuario }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{{ sol.nome_paciente }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.leito || 'Não especificado' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.solicitante }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ sol.itens.length }} item(ns)
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium flex items-center space-x-2">
                  <Button @click="abrirAuditoria(sol)" size="sm" variant="primary">Auditar</Button>
                  <div class="relative group inline-block">
                    <Button @click="visualizarDetalhes(sol)" size="sm" variant="default" class="p-1.5">
                      <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </Button>
                    <span class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-slate-800 text-white text-xs py-1 px-2 rounded whitespace-nowrap z-50">
                      Ver detalhes
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>

    <!-- Conteúdo da Aba Farmácia -->
    <div v-if="abaAtiva === 'farmacia'" class="space-y-4">
      <Card>
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-semibold text-slate-700">Painel de Liberação - Farmácia</h2>
            <span class="text-xs text-slate-500">Apenas membros com perfil de farmácia (SOL-COB-FARMACIA) podem liberar</span>
          </div>
        </template>
        
        <div v-if="loading" class="py-12 flex justify-center">
          <LoadingIndicator />
        </div>
        <div v-else-if="solicitacoesAutorizadas.length === 0" class="py-12 text-center text-slate-500">
          Nenhuma solicitação autorizada aguardando entrega.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Prontuário</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Paciente</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Leito</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Auditor CCIRAS</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Itens Autorizados</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-200">
              <tr v-for="sol in solicitacoesAutorizadas" :key="sol.id" class="hover:bg-slate-50 transition-colors duration-150">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-900">{{ sol.prontuario }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{{ sol.nome_paciente }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.leito || 'Não especificado' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.auditor_username }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                  <div v-for="item in sol.itens.filter(i => i.status_item === 'AUTORIZADO')" :key="item.id">
                    • {{ item.nome_material }} (Qtd: {{ item.quantidade_autorizada }})
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium flex items-center space-x-2">
                  <Button @click="confirmarEntrega(sol)" size="sm" variant="success">Liberado</Button>
                  <div class="relative group inline-block">
                    <Button @click="visualizarDetalhes(sol)" size="sm" variant="default" class="p-1.5">
                      <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </Button>
                    <span class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-slate-800 text-white text-xs py-1 px-2 rounded whitespace-nowrap z-50">
                      Ver detalhes
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>

    <!-- Conteúdo da Aba Histórico -->
    <div v-if="abaAtiva === 'historico'" class="space-y-4">
      <Card>
        <template #header>
          <h2 class="text-lg font-semibold text-slate-700">Histórico Completo</h2>
        </template>
        
        <div v-if="loading" class="py-12 flex justify-center">
          <LoadingIndicator />
        </div>
        <div v-else-if="historicoSolicitacoes.length === 0" class="py-12 text-center text-slate-500">
          Nenhuma solicitação cadastrada no histórico.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Prontuário</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Paciente</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Solicitante</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Data Solicitação</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-200">
              <tr v-for="sol in historicoSolicitacoes" :key="sol.id" class="hover:bg-slate-50 transition-colors duration-150">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-900">{{ sol.prontuario }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{{ sol.nome_paciente }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.solicitante }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ formatarData(sol.created_at) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <span :class="getStatusBadgeClass(sol.status)">
                    {{ sol.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="relative group inline-block">
                    <Button @click="visualizarDetalhes(sol)" size="sm" variant="default" class="p-1.5">
                      <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </Button>
                    <span class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-slate-800 text-white text-xs py-1 px-2 rounded whitespace-nowrap z-50">
                      Ver detalhes
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>

    <!-- Modal de Auditoria CCIRAS -->
    <Modal :show="showAuditoriaModal" @close="showAuditoriaModal = false">
      <template #header>
        Auditar Solicitação - Paciente: {{ solicitacaoSelecionada?.nome_paciente }}
      </template>

      <div class="space-y-6 py-2" v-if="solicitacaoSelecionada">
        <div class="grid grid-cols-2 gap-4 text-sm bg-slate-50 p-4 rounded-lg border border-slate-100">
          <div><span class="font-medium text-slate-500">Prontuário:</span> {{ solicitacaoSelecionada.prontuario }}</div>
          <div><span class="font-medium text-slate-500">Leito:</span> {{ solicitacaoSelecionada.leito || 'N/A' }}</div>
          <div><span class="font-medium text-slate-500">Solicitante:</span> {{ solicitacaoSelecionada.solicitante }}</div>
          <div><span class="font-medium text-slate-500">Data de Entrada:</span> {{ formatarData(solicitacaoSelecionada.created_at) }}</div>
        </div>

        <div>
          <h3 class="font-semibold text-slate-700 mb-3">Itens Solicitados</h3>
          <div class="space-y-4">
            <div v-for="item in auditoriaItens" :key="item.id" class="border border-slate-200 rounded-lg p-4 bg-white flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div class="flex-1">
                <p class="font-medium text-slate-900">{{ item.nome_material }}</p>
                <p class="text-xs text-slate-500">Código: {{ item.codigo_material }} | Qtd. Solicitada: <span class="font-semibold">{{ item.quantidade_solicitada }}</span></p>
              </div>
              <div class="flex items-center gap-4">
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Status Item</label>
                  <select v-model="item.status_item" class="form-control text-sm py-1 min-w-[130px]">
                    <option value="AUTORIZADO">Autorizar</option>
                    <option value="NEGADO">Negar</option>
                    <option value="PENDENTE">Pendente</option>
                  </select>
                </div>
                <div v-if="item.status_item === 'AUTORIZADO'">
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Qtd. Autorizada</label>
                  <input type="number" v-model.number="item.quantidade_autorizada" min="0" :max="item.quantidade_solicitada" class="form-control text-sm py-1 w-20">
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Justificativa / Parecer CCIRAS</label>
          <textarea v-model="auditoriaJustificativa" rows="3" class="form-control" placeholder="Descreva os motivos da decisão ou observações pertinentes..."></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">Decisão Geral da Solicitação</label>
          <div class="flex flex-wrap gap-4 mt-2">
            <label class="inline-flex items-center">
              <input type="radio" v-model="auditoriaStatusGeral" value="LIBERADO PELA CCIRAS" class="form-radio text-indigo-600">
              <span class="ml-2 text-sm text-slate-700">Liberado pela CCIRAS</span>
            </label>
            <label class="inline-flex items-center">
              <input type="radio" v-model="auditoriaStatusGeral" value="EM ANÁLISE" class="form-radio text-yellow-600">
              <span class="ml-2 text-sm text-slate-700">Em Análise</span>
            </label>
            <label class="inline-flex items-center">
              <input type="radio" v-model="auditoriaStatusGeral" value="NEGADO" class="form-radio text-red-600">
              <span class="ml-2 text-sm text-slate-700">Negado</span>
            </label>
          </div>
        </div>
      </div>

      <template #footer>
        <Button @click="showAuditoriaModal = false" variant="default">Cancelar</Button>
        <Button @click="salvarAuditoria" variant="primary" :disabled="salvandoAuditoria">Salvar Auditoria</Button>
      </template>
    </Modal>

    <!-- Modal de Detalhes da Solicitação -->
    <Modal :show="showDetalhesModal" @close="showDetalhesModal = false">
      <template #header>
        Detalhes da Solicitação #{{ solicitacaoSelecionada?.id }}
      </template>

      <div class="space-y-6 py-2" v-if="solicitacaoSelecionada">
        <div class="grid grid-cols-2 gap-4 text-sm bg-slate-50 p-4 rounded-lg border border-slate-100">
          <div><span class="font-medium text-slate-500">Status Geral:</span> <span :class="getStatusBadgeClass(solicitacaoSelecionada.status)">{{ solicitacaoSelecionada.status }}</span></div>
          <div><span class="font-medium text-slate-500">Prontuário:</span> {{ solicitacaoSelecionada.prontuario }}</div>
          <div><span class="font-medium text-slate-500">Paciente:</span> {{ solicitacaoSelecionada.nome_paciente }}</div>
          <div><span class="font-medium text-slate-500">Leito:</span> {{ solicitacaoSelecionada.leito || 'N/A' }}</div>
          <div><span class="font-medium text-slate-500">Solicitante:</span> {{ solicitacaoSelecionada.solicitante }}</div>
          <div><span class="font-medium text-slate-500">Data Solicitação:</span> {{ formatarData(solicitacaoSelecionada.created_at) }}</div>
        </div>

        <!-- Seção CCIRAS -->
        <div v-if="solicitacaoSelecionada.auditor_username" class="border border-indigo-100 bg-indigo-50/30 rounded-lg p-4 space-y-2">
          <h3 class="font-semibold text-indigo-900 text-sm">Parecer da Auditoria CCIRAS</h3>
          <div class="grid grid-cols-2 gap-2 text-xs text-indigo-950">
            <div><span class="font-medium">Auditor:</span> {{ solicitacaoSelecionada.auditor_username }}</div>
            <div><span class="font-medium">Data:</span> {{ formatarData(solicitacaoSelecionada.data_auditoria) }}</div>
          </div>
          <p class="text-sm text-indigo-950 mt-1 italic">"{{ solicitacaoSelecionada.justificativa }}"</p>
        </div>

        <!-- Seção Farmácia -->
        <div v-if="solicitacaoSelecionada.farmaceutico_username" class="border border-green-100 bg-green-50/30 rounded-lg p-4 space-y-2">
          <h3 class="font-semibold text-green-900 text-sm">Registro de Liberação / Farmácia</h3>
          <div class="grid grid-cols-2 gap-2 text-xs text-green-950">
            <div><span class="font-medium">Farmacêutico:</span> {{ solicitacaoSelecionada.farmaceutico_username }}</div>
            <div><span class="font-medium">Data Entrega:</span> {{ formatarData(solicitacaoSelecionada.data_entrega) }}</div>
          </div>
        </div>

        <div>
          <h3 class="font-semibold text-slate-700 mb-2">Itens da Solicitação</h3>
          <ul class="divide-y divide-slate-100 border border-slate-200 rounded-lg bg-white overflow-hidden">
            <li v-for="item in solicitacaoSelecionada.itens" :key="item.id" class="p-3 flex justify-between items-center text-sm">
              <div>
                <p class="font-medium text-slate-900">{{ item.nome_material }}</p>
                <p class="text-xs text-slate-500">Solicitado: {{ item.quantidade_solicitada }}</p>
              </div>
              <div class="text-right">
                <span :class="getStatusBadgeClass(item.status_item)">
                  {{ item.status_item }}
                </span>
                <p v-if="item.status_item === 'AUTORIZADO'" class="text-xs text-slate-600 mt-1">Autorizado: {{ item.quantidade_autorizada }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <template #footer>
        <Button @click="showDetalhesModal = false" variant="default">Fechar</Button>
      </template>
    </Modal>

    <!-- Modal Simulador de Inserção de Dados do AGHU -->
    <Modal :show="showSimuladorModal" @close="showSimuladorModal = false">
      <template #header>
        Simulador de Carga do AGHU
      </template>

      <div class="space-y-4 py-2">
        <p class="text-sm text-slate-500">
          Como a criação de solicitações vem diretamente do AGHU por banco ou API, use este painel para enviar uma nova solicitação simulada ao sistema.
        </p>

        <div class="form-group">
          <label class="form-label">Paciente de Teste</label>
          <select v-model="pacienteSimulado" class="form-control">
            <option v-for="pac in pacientesDiposniveis" :key="pac.codigo" :value="pac">
              {{ pac.nome }} (Prontuário: {{ pac.codigo }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Leito / Setor</label>
          <input type="text" v-model="leitoSimulado" class="form-control" placeholder="Ex: Leito 402 - Ala Norte">
        </div>

        <div class="form-group">
          <label class="form-label">Solicitante (Profissional AGHU)</label>
          <input type="text" v-model="solicitanteSimulado" class="form-control" placeholder="Nome do médico/enfermeiro">
        </div>

        <div>
          <label class="block text-sm font-semibold text-slate-700 mb-2">Selecione as Coberturas Especiais</label>
          <div class="space-y-2 max-h-48 overflow-y-auto border border-slate-200 rounded-lg p-3 bg-slate-50">
            <div v-for="mat in materiaisPredefinidos" :key="mat.codigo" class="flex items-center justify-between">
              <label class="flex items-center text-sm text-slate-700 cursor-pointer">
                <input type="checkbox" :value="mat" v-model="materiaisSelecionadosSimulado" class="form-checkbox text-indigo-600 rounded">
                <span class="ml-2">{{ mat.nome }}</span>
              </label>
              <div v-if="materiaisSelecionadosSimulado.some(m => m.codigo === mat.codigo)" class="flex items-center gap-2">
                <span class="text-xs text-slate-500">Qtd:</span>
                <input type="number" v-model.number="mat.qtd" min="1" class="form-control py-0.5 px-1.5 w-14 text-center text-xs">
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <Button @click="showSimuladorModal = false" variant="default">Cancelar</Button>
        <Button @click="enviarSolicitacaoSimulada" variant="primary" :disabled="simulandoCarga">Enviar Solicitação</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useToast } from 'vue-toastification';
import SolicitacoesService, { SolicitacaoCobertura } from '../services/SolicitacoesService';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import LoadingIndicator from '../components/LoadingIndicator.vue';

const toast = useToast();

const abas = ref([
  { id: 'cciras', nome: 'CCIRAS (Auditoria)', badge: 0 },
  { id: 'farmacia', nome: 'Farmácia (Liberação)', badge: 0 },
  { id: 'historico', nome: 'Histórico Completo' }
]);
const abaAtiva = ref('cciras');

const loading = ref(false);
const solicitacoes = ref<SolicitacaoCobertura[]>([]);

// Listas filtradas
const solicitacoesPendentes = computed(() => solicitacoes.value.filter(s => s.status === 'PENDENTE' || s.status === 'EM ANÁLISE'));
const solicitacoesAutorizadas = computed(() => solicitacoes.value.filter(s => s.status === 'AUTORIZADO' || s.status === 'LIBERADO PELA CCIRAS'));
const historicoSolicitacoes = computed(() => solicitacoes.value);

// Atualização de badges das abas
const atualizarBadges = () => {
  abas.value[0].badge = solicitacoesPendentes.value.length;
  abas.value[1].badge = solicitacoesAutorizadas.value.length;
};

// Carregamento de dados
const carregarSolicitacoes = async () => {
  loading.value = true;
  try {
    solicitacoes.value = await SolicitacoesService.listar();
    atualizarBadges();
  } catch (err: any) {
    toast.error('Erro ao carregar solicitações.');
  } finally {
    loading.value = false;
  }
};

// Auditoria CCIRAS
const showAuditoriaModal = ref(false);
const solicitacaoSelecionada = ref<SolicitacaoCobertura | null>(null);
const auditoriaStatusGeral = ref('LIBERADO PELA CCIRAS');
const auditoriaJustificativa = ref('');
const auditoriaItens = ref<any[]>([]);
const salvandoAuditoria = ref(false);

const abrirAuditoria = (sol: SolicitacaoCobertura) => {
  solicitacaoSelecionada.value = sol;
  auditoriaStatusGeral.value = sol.status === 'EM ANÁLISE' ? 'EM ANÁLISE' : 'LIBERADO PELA CCIRAS';
  auditoriaJustificativa.value = sol.justificativa || '';
  auditoriaItens.value = sol.itens.map(item => ({
    ...item,
    status_item: item.status_item || 'AUTORIZADO',
    quantidade_autorizada: item.quantidade_autorizada !== undefined && item.quantidade_autorizada !== null ? item.quantidade_autorizada : item.quantidade_solicitada
  }));
  showAuditoriaModal.value = true;
};

const salvarAuditoria = async () => {
  if (!solicitacaoSelecionada.value?.id) return;
  if (!auditoriaJustificativa.value.trim()) {
    toast.warning('Por favor, informe uma justificativa/parecer da auditoria.');
    return;
  }

  salvandoAuditoria.value = true;
  try {
    const payload = {
      status_geral: auditoriaStatusGeral.value,
      justificativa: auditoriaJustificativa.value,
      itens: auditoriaItens.value.map(i => ({
        id: i.id!,
        quantidade_autorizada: i.status_item === 'AUTORIZADO' ? i.quantidade_autorizada : 0,
        status_item: i.status_item
      }))
    };

    await SolicitacoesService.auditar(solicitacaoSelecionada.value.id, payload);
    toast.success('Auditoria registrada com sucesso!');
    showAuditoriaModal.value = false;
    await carregarSolicitacoes();
  } catch (err: any) {
    const detail = err.response?.data?.detail || 'Erro ao salvar auditoria.';
    toast.error(detail);
  } finally {
    salvandoAuditoria.value = false;
  }
};

// Entrega Farmácia
const confirmarEntrega = async (sol: SolicitacaoCobertura) => {
  if (!sol.id) return;
  if (!confirm(`Confirmar liberação e entrega das coberturas para o paciente ${sol.nome_paciente}?`)) return;

  try {
    await SolicitacoesService.entregar(sol.id);
    toast.success('Entrega e liberação de itens registradas!');
    await carregarSolicitacoes();
  } catch (err: any) {
    const detail = err.response?.data?.detail || 'Erro ao registrar entrega.';
    toast.error(detail);
  }
};

// Visualização de detalhes
const showDetalhesModal = ref(false);
const visualizarDetalhes = (sol: SolicitacaoCobertura) => {
  solicitacaoSelecionada.value = sol;
  showDetalhesModal.value = true;
};

// Simulador de Carga de Dados do AGHU
const showSimuladorModal = ref(false);
const simulandoCarga = ref(false);
const pacientesDiposniveis = ref<any[]>([]);
const pacienteSimulado = ref<any>(null);
const leitoSimulado = ref('Leito 203 - Ala B');
const solicitanteSimulado = ref('Dr. Roberto Albuquerque');
const materiaisSelecionadosSimulado = ref<any[]>([]);

const materiaisPredefinidos = ref([
  { codigo: 10201, nome: 'Placa de Hidrocolóide 10x10', qtd: 5 },
  { codigo: 10202, nome: 'Alginato de Cálcio (Fita)', qtd: 3 },
  { codigo: 10203, nome: 'Cobertura de Prata Nanocristalina 15x15', qtd: 2 },
  { codigo: 10204, nome: 'Curativo de Espuma de Poliuretano', qtd: 4 },
  { codigo: 10205, nome: 'Gel de Limpeza de Feridas (Hydrogel)', qtd: 2 }
]);

const carregarPacientesParaSimulador = async () => {
  try {
    const { data } = await api.get('/api/pacientes');
    pacientesDiposniveis.value = data;
    if (data.length > 0) {
      pacienteSimulado.value = data[0];
    }
  } catch (e) {
    console.error('Erro ao listar pacientes para simulação', e);
  }
};

const enviarSolicitacaoSimulada = async () => {
  if (!pacienteSimulado.value) {
    toast.error('Nenhum paciente selecionado para simular.');
    return;
  }
  if (materiaisSelecionadosSimulado.value.length === 0) {
    toast.error('Selecione ao menos um item de cobertura.');
    return;
  }

  simulandoCarga.value = true;
  try {
    const payload: SolicitacaoCobertura = {
      prontuario: pacienteSimulado.value.codigo,
      nome_paciente: pacienteSimulado.value.nome,
      leito: leitoSimulado.value,
      solicitante: solicitanteSimulado.value,
      itens: materiaisSelecionadosSimulado.value.map(mat => ({
        codigo_material: mat.codigo,
        nome_material: mat.nome,
        quantidade_solicitada: mat.qtd
      }))
    };

    await SolicitacoesService.criarMock(payload);
    toast.success('Solicitação simulada enviada com sucesso ao painel!');
    showSimuladorModal.value = false;
    // Limpa seleções
    materials: materiaisSelecionadosSimulado.value = [];
    await carregarSolicitacoes();
  } catch (err: any) {
    toast.error('Falha ao simular envio de dados do AGHU.');
  } finally {
    simulandoCarga.value = false;
  }
};

// Helpers de estilo e formatação
const formatarData = (dataStr?: string | null) => {
  if (!dataStr) return 'N/A';
  const data = new Date(dataStr);
  return data.toLocaleString('pt-BR');
};

const getStatusBadgeClass = (status?: string) => {
  switch (status?.toUpperCase()) {
    case 'PENDENTE':
      return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-800';
    case 'EM ANÁLISE':
      return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-orange-100 text-orange-800';
    case 'AUTORIZADO':
    case 'LIBERADO PELA CCIRAS':
      return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-green-100 text-green-800';
    case 'NEGADO':
      return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-red-100 text-red-800';
    case 'ENTREGUE':
      return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800';
    default:
      return 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800';
  }
};

onMounted(() => {
  carregarSolicitacoes();
  carregarPacientesParaSimulador();
});
</script>
