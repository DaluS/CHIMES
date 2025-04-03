// src/pages/ModelDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Button, 
  CircularProgress, 
  Grid, 
  Chip, 
  Divider, 
  List,
  ListItem,
  ListItemText,
  Paper,
  Tab,
  Tabs,
  IconButton,
  Tooltip,
  Avatar,
  Stack,
  LinearProgress,
  Fade,
  Alert
} from '@mui/material';
import axios from 'axios';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import InfoIcon from '@mui/icons-material/Info';
import CodeIcon from '@mui/icons-material/Code';
import SchemaIcon from '@mui/icons-material/Schema';
import DataObjectIcon from '@mui/icons-material/DataObject';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import SettingsIcon from '@mui/icons-material/Settings';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import HistoryIcon from '@mui/icons-material/History';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ShareIcon from '@mui/icons-material/Share';
import DownloadIcon from '@mui/icons-material/Download';

const API_URL = 'http://localhost:8000';

// Composant pour l'affichage des onglets
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`model-tabpanel-${index}`}
      aria-labelledby={`model-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ py: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

// Composant pour afficher du code
const CodeBlock = ({ code, language = 'json', title }) => {
  return (
    <Box sx={{ position: 'relative', mb: 3 }}>
      {title && (
        <Box sx={{ mb: 1, display: 'flex', alignItems: 'center' }}>
          <CodeIcon sx={{ mr: 1, color: 'text.secondary' }} />
          <Typography variant="subtitle2" color="text.secondary">
            {title}
          </Typography>
        </Box>
      )}
      <Paper
        sx={{
          bgcolor: 'background.default',
          p: 2,
          borderRadius: 2,
          fontFamily: 'monospace',
          position: 'relative',
          fontSize: '0.875rem',
          overflowX: 'auto',
        }}
      >
        <IconButton
          onClick={() => navigator.clipboard.writeText(code)}
          sx={{
            position: 'absolute',
            top: 8,
            right: 8,
            bgcolor: 'background.paper',
            '&:hover': { bgcolor: 'background.card' },
          }}
          size="small"
        >
          <ContentCopyIcon fontSize="small" />
        </IconButton>
        <pre style={{ margin: 0 }}>{code}</pre>
      </Paper>
    </Box>
  );
};

const ModelDetailPage = () => {
  const { modelName } = useParams();
  const navigate = useNavigate();
  const [modelDetails, setModelDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [selectedPreset, setSelectedPreset] = useState('');
  
  useEffect(() => {
    const fetchModelDetails = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}/models/${modelName}`);
        setModelDetails(response.data);
        
        // Set default preset if available
        if (response.data.presets && Object.keys(response.data.presets).length > 0) {
          setSelectedPreset(Object.keys(response.data.presets)[0]);
        }
      } catch (err) {
        console.error('Error fetching model details:', err);
        setError(`Impossible de charger les détails du modèle ${modelName}.`);
      } finally {
        setLoading(false);
      }
    };
    
    fetchModelDetails();
  }, [modelName]);
  
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  const handleCopyCode = (text) => {
    navigator.clipboard.writeText(text);
    // Todo: Show notification
  };
  
  const handleStartSimulation = async () => {
    try {
      // Dans une application complète, ceci créerait une session et naviguerait vers une page de simulation
      alert('Fonctionnalité de simulation en cours de développement');
    } catch (err) {
      console.error('Error starting simulation:', err);
    }
  };
  
  if (loading) {
    return (
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center', 
        justifyContent: 'center', 
        minHeight: '60vh' 
      }}>
        <CircularProgress size={60} thickness={4} />
        <Typography variant="h6" sx={{ mt: 3, color: 'text.secondary' }}>
          Chargement du modèle...
        </Typography>
      </Box>
    );
  }
  
  if (error || !modelDetails) {
    return (
      <Box sx={{ textAlign: 'center', my: 4 }}>
        <Alert 
          severity="error" 
          sx={{ 
            maxWidth: 600, 
            mx: 'auto',
            mb: 3,
            bgcolor: 'rgba(248, 114, 114, 0.1)',
            border: '1px solid rgba(248, 114, 114, 0.2)',
          }}
        >
          {error || `Le modèle ${modelName} n'a pas pu être chargé.`}
        </Alert>
        <Button 
          variant="contained" 
          onClick={() => navigate('/models')}
          startIcon={<ArrowBackIcon />}
        >
          Retour aux modèles
        </Button>
      </Box>
    );
  }
  
  return (
    <Fade in={!loading}>
      <Box>
        <Box sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
          <Button 
            variant="text" 
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/models')}
            sx={{ mr: 2 }}
          >
            Retour
          </Button>
          <Typography 
            variant="h4" 
            component="h1" 
            sx={{
              fontWeight: 700,
              flexGrow: 1,
            }}
          >
            {modelName}
          </Typography>
          <Box>
            <Tooltip title="Partager">
              <IconButton sx={{ mx: 0.5 }}>
                <ShareIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Télécharger">
              <IconButton sx={{ mx: 0.5 }}>
                <DownloadIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Ajouter aux favoris">
              <IconButton sx={{ mx: 0.5 }}>
                <FavoriteBorderIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="body1" color="text.secondary">
            {modelDetails.summary?.description || "Aucune description disponible"}
          </Typography>
        </Box>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <Box sx={{ borderBottom: 1, borderColor: 'divider', px: 2, pt: 1 }}>
                <Tabs 
                  value={activeTab} 
                  onChange={handleTabChange} 
                  aria-label="model information tabs"
                  variant="scrollable"
                  scrollButtons="auto"
                >
                  <Tab 
                    icon={<InfoIcon />} 
                    iconPosition="start" 
                    label="Aperçu" 
                    id="model-tab-0" 
                    aria-controls="model-tabpanel-0" 
                  />
                  <Tab 
                    icon={<DataObjectIcon />} 
                    iconPosition="start" 
                    label="Paramètres" 
                    id="model-tab-1" 
                    aria-controls="model-tabpanel-1" 
                  />
                  <Tab 
                    icon={<CodeIcon />} 
                    iconPosition="start" 
                    label="API" 
                    id="model-tab-2" 
                    aria-controls="model-tabpanel-2" 
                  />
                  <Tab 
                    icon={<SchemaIcon />} 
                    iconPosition="start" 
                    label="Schéma" 
                    id="model-tab-3" 
                    aria-controls="model-tabpanel-3" 
                  />
                  <Tab 
                    icon={<HistoryIcon />} 
                    iconPosition="start" 
                    label="Historique" 
                    id="model-tab-4" 
                    aria-controls="model-tabpanel-4" 
                  />
                </Tabs>
              </Box>
              
              <CardContent>
                <TabPanel value={activeTab} index={0}>
                  <Typography variant="h6" gutterBottom>
                    Description
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {modelDetails.summary?.long_description || modelDetails.summary?.description || "Aucune description détaillée disponible pour ce modèle."}
                  </Typography>
                  
                  {modelDetails.summary?.references && (
                    <>
                      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                        Références
                      </Typography>
                      <List sx={{ bgcolor: 'background.default', borderRadius: 2 }}>
                        {modelDetails.summary.references.map((reference, index) => (
                          <ListItem key={index} sx={{ py: 1 }}>
                            <ListItemText primary={reference} />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}
                  
                  {modelDetails.summary?.examples && (
                    <>
                      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                        Exemples d'utilisation
                      </Typography>
                      <Paper sx={{ p: 2, bgcolor: 'background.default', borderRadius: 2 }}>
                        <pre style={{ margin: 0, fontFamily: 'monospace', fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>
                          {modelDetails.summary.examples}
                        </pre>
                      </Paper>
                    </>
                  )}
                </TabPanel>
                
                <TabPanel value={activeTab} index={1}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h6">
                      Paramètres du modèle
                    </Typography>
                    
                    {modelDetails.presets && Object.keys(modelDetails.presets).length > 0 && (
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="body2" color="text.secondary" sx={{ mr: 2 }}>
                          Préréglages:
                        </Typography>
                        <Stack direction="row" spacing={1}>
                          {Object.keys(modelDetails.presets).map((preset) => (
                            <Chip
                              key={preset}
                              label={preset}
                              variant={selectedPreset === preset ? "filled" : "outlined"}
                              color="primary"
                              clickable
                              onClick={() => setSelectedPreset(preset)}
                              size="small"
                            />
                          ))}
                        </Stack>
                      </Box>
                    )}
                  </Box>
                  
                  <Paper sx={{ p: 2, bgcolor: 'background.default', borderRadius: 2 }}>
                    <List>
                      {Object.entries(modelDetails.fields || {})
                        .filter(([key, field]) => field.eqtype === 'parameter')
                        .map(([key, field]) => (
                          <ListItem 
                            key={key} 
                            sx={{ 
                              borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
                              py: 2 
                            }}
                          >
                            <Grid container spacing={2}>
                              <Grid item xs={12} sm={4}>
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                  <Typography variant="subtitle2" fontFamily="monospace">
                                    {key}
                                  </Typography>
                                  {field.units && (
                                    <Chip 
                                      label={field.units} 
                                      size="small" 
                                      variant="outlined"
                                      sx={{ ml: 1 }}
                                    />
                                  )}
                                </Box>
                                {field.type && (
                                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                                    Type: <span style={{ fontFamily: 'monospace' }}>{field.type}</span>
                                  </Typography>
                                )}
                              </Grid>
                              <Grid item xs={12} sm={8}>
                                <Typography variant="body2">
                                  {field.definition || "Aucune définition disponible"}
                                </Typography>
                                {field.range && (
                                  <Box sx={{ mt: 1, display: 'flex', alignItems: 'center' }}>
                                    <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
                                      Plage: {field.range[0]} - {field.range[1]}
                                    </Typography>
                                    <LinearProgress 
                                      variant="determinate" 
                                      value={50} 
                                      sx={{ flexGrow: 1, height: 8, borderRadius: 4 }}
                                    />
                                  </Box>
                                )}
                                {field.default !== undefined && (
                                  <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                                    Valeur par défaut: <span style={{ fontFamily: 'monospace' }}>{field.default}</span>
                                  </Typography>
                                )}
                              </Grid>
                            </Grid>
                          </ListItem>
                        ))}
                    </List>
                  </Paper>
                </TabPanel>
                
                <TabPanel value={activeTab} index={2}>
                  <Typography variant="h6" gutterBottom>
                    Utilisation de l'API
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Intégrez ce modèle dans vos applications avec l'API CHIMES.
                  </Typography>
                  
                  <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
                    Requête
                  </Typography>
                  <CodeBlock
                    title="GET /models/{modelName}"
                    code={`curl -X GET "${API_URL}/models/${modelName}" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY"`}
                    language="bash"
                  />
                  
                  <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
                    Simulation
                  </Typography>
                  <CodeBlock
                    title="POST /simulations"
                    code={`curl -X POST "${API_URL}/simulations" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "model": "${modelName}",
    "parameters": {
      // Your parameters here
    },
    "timespan": {
      "start": 0,
      "end": 100,
      "step": 1
    }
  }'`}
                    language="bash"
                  />
                  
                  <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
                    Exemple en Python
                  </Typography>
                  <CodeBlock
                    language="python"
                    code={`import requests
import json

# Configuration
api_url = "${API_URL}"
api_key = "YOUR_API_KEY"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Créer une simulation
simulation_data = {
    "model": "${modelName}",
    "parameters": {
        # Paramètres du modèle
    },
    "timespan": {
        "start": 0,
        "end": 100,
        "step": 1
    }
}

# Lancer la simulation
response = requests.post(
    f"{api_url}/simulations",
    headers=headers,
    data=json.dumps(simulation_data)
)

# Récupérer l'ID de la simulation
simulation_id = response.json()["id"]

# Récupérer les résultats
results = requests.get(
    f"{api_url}/simulations/{simulation_id}/results",
    headers=headers
)

print(results.json())`}
                  />
                </TabPanel>
                
                <TabPanel value={activeTab} index={3}>
                  <Typography variant="h6" gutterBottom>
                    Schéma du modèle
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Structure et relations des composants du modèle.
                  </Typography>
                  
                  <Paper 
                    sx={{ 
                      p: 3, 
                      bgcolor: 'background.default', 
                      borderRadius: 2,
                      height: '400px',
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center'
                    }}
                  >
                    <Box sx={{ textAlign: 'center' }}>
                      <SchemaIcon sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
                      <Typography variant="body1" color="text.secondary">
                        Visualisation du schéma en cours de développement
                      </Typography>
                    </Box>
                  </Paper>
                  
                  <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
                    Structure JSON
                  </Typography>
                  <CodeBlock
                    language="json"
                    code={JSON.stringify(modelDetails, null, 2)}
                  />
                </TabPanel>
                
                <TabPanel value={activeTab} index={4}>
                  <Typography variant="h6" gutterBottom>
                    Historique des versions
                  </Typography>
                  
                  <List>
                    <ListItem 
                      sx={{ 
                        mb: 2, 
                        bgcolor: 'background.default', 
                        borderRadius: 2,
                        border: '1px solid rgba(255, 255, 255, 0.05)'
                      }}
                    >
                      <Box sx={{ width: '100%' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32, mr: 1.5, fontSize: '0.875rem' }}>1.0</Avatar>
                          <Typography variant="subtitle1" fontWeight={600}>
                            Version 1.0
                          </Typography>
                          <Chip 
                            label="Actuelle" 
                            size="small" 
                            color="success" 
                            sx={{ ml: 2 }}
                          />
                          <Typography variant="caption" color="text.secondary" sx={{ ml: 'auto' }}>
                            14/03/2023
                          </Typography>
                        </Box>
                        <Typography variant="body2">
                          Version initiale du modèle.
                        </Typography>
                      </Box>
                    </ListItem>
                    
                    <ListItem 
                      sx={{ 
                        bgcolor: 'background.default', 
                        borderRadius: 2,
                        border: '1px solid rgba(255, 255, 255, 0.05)',
                        opacity: 0.6
                      }}
                    >
                      <Box sx={{ width: '100%' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Avatar sx={{ bgcolor: 'text.disabled', width: 32, height: 32, mr: 1.5, fontSize: '0.875rem' }}>0.9</Avatar>
                          <Typography variant="subtitle1" fontWeight={600}>
                            Version 0.9 (Beta)
                          </Typography>
                          <Typography variant="caption" color="text.secondary" sx={{ ml: 'auto' }}>
                            28/02/2023
                          </Typography>
                        </Box>
                        <Typography variant="body2">
                          Version beta avec les fonctionnalités principales.
                        </Typography>
                      </Box>
                    </ListItem>
                  </List>
                </TabPanel>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Lancer une simulation
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Configurez et lancez une simulation avec ce modèle.
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  size="large"
                  startIcon={<PlayArrowIcon />}
                  onClick={handleStartSimulation}
                  sx={{ mt: 2 }}
                >
                  Démarrer la simulation
                </Button>
                
                <Typography variant="body2" color="text.secondary" sx={{ mt: 4, mb: 1 }}>
                  Options avancées
                </Typography>
                <Button
                  variant="outlined"
                  color="inherit"
                  fullWidth
                  startIcon={<SettingsIcon />}
                  sx={{ mb: 1 }}
                >
                  Configurer les paramètres
                </Button>
              </CardContent>
            </Card>
            
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Informations
                </Typography>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Type
                </Typography>
                <Typography variant="body1" paragraph>
                  {modelDetails.summary?.type || "Non spécifié"}
                </Typography>
                
                <Divider sx={{ my: 1 }} />
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Mots-clés
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                  {(modelDetails.summary?.keywords || []).map((keyword, index) => (
                    <Chip 
                      key={index} 
                      label={keyword} 
                      size="small" 
                      color="primary" 
                      variant="outlined"
                    />
                  ))}
                </Box>
                
                <Divider sx={{ my: 1 }} />
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Auteur
                </Typography>
                <Typography variant="body1" paragraph>
                  {modelDetails.summary?.author || "Non spécifié"}
                </Typography>
                
                <Divider sx={{ my: 1 }} />
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Version
                </Typography>
                <Typography variant="body1" paragraph>
                  {modelDetails.summary?.version || "1.0.0"}
                </Typography>
                
                <Divider sx={{ my: 1 }} />
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Date de création
                </Typography>
                <Typography variant="body1">
                  {modelDetails.summary?.created || "Non spécifiée"}
                </Typography>
              </CardContent>
            </Card>
            
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Modèles similaires
                </Typography>
                
                <List sx={{ px: 0 }}>
                  {['EconomicModel', 'ClimateModel', 'EcosystemModel'].map((modelName) => (
                    <ListItem 
                      key={modelName}
                      sx={{ 
                        px: 2, 
                        py: 1.5, 
                        borderRadius: 2,
                        '&:hover': { bgcolor: 'background.default' },
                        mb: 1
                      }}
                      button
                      onClick={() => navigate(`/models/${modelName}`)}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <Avatar 
                          sx={{ 
                            bgcolor: 'primary.dark', 
                            width: 36, 
                            height: 36, 
                            mr: 1.5,
                            fontSize: '1rem'
                          }}
                        >
                          {modelName.substring(0, 1)}
                        </Avatar>
                        <Box>
                          <Typography variant="body1" fontWeight={500}>
                            {modelName}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Modèle {modelName === 'EconomicModel' ? 'économique' : modelName === 'ClimateModel' ? 'climatique' : 'écosystémique'}
                          </Typography>
                        </Box>
                      </Box>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Fade>
  );
};

export default ModelDetailPage;