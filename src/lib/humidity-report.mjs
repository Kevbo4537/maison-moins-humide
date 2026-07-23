const round1 = (value) => Math.round(value * 10) / 10;

function isCompleteReading(reading) {
  return reading?.temp !== null
    && reading?.temp !== ''
    && reading?.rh !== null
    && reading?.rh !== ''
    && Number.isFinite(Number(reading.temp))
    && Number.isFinite(Number(reading.rh))
    && Number(reading.rh) >= 20
    && Number(reading.rh) <= 100
    && Number(reading.temp) >= 0
    && Number(reading.temp) <= 40;
}

function longestStreak(values, predicate) {
  let longest = 0;
  let current = 0;
  for (const value of values) {
    current = predicate(value) ? current + 1 : 0;
    longest = Math.max(longest, current);
  }
  return longest;
}

function mean(values) {
  return values.reduce((total, value) => total + value, 0) / values.length;
}

function readingContextMap(contexts = []) {
  return new Map(contexts.map((item) => {
    const rawEvents = Array.isArray(item.events) ? item.events : [item.event || 'none'];
    return [Number(item.day), new Set(rawEvents.filter(Boolean))];
  }));
}

function contextHas(contextMap, day, event) {
  return contextMap.get(Number(day))?.has(event) || false;
}

function dayHasHighReading(readings, day) {
  return readings.some((reading) => Number(reading.day) === day && Number(reading.rh) > 60);
}

const PROFILES = {
  reassuring: {
    code: 'reassuring',
    title: 'Suivi rassurant',
    description: 'Les mesures ne montrent pas d’excès durable et aucun signe d’eau ou de moisissure n’a été déclaré.',
  },
  'high-comfort-zone': {
    code: 'high-comfort-zone',
    title: 'Humidité stable dans la zone haute — à surveiller',
    description: 'Les valeurs restent souvent entre 55 et 60 %. Ce n’est pas un dépassement franc, mais leur répétition mérite d’être visible plutôt que résumée par deux compteurs à zéro.',
  },
  'activity-peaks': {
    code: 'activity-peaks',
    title: 'Pics liés aux activités',
    description: 'Les hausses sont brèves et coïncident surtout avec douche, cuisson ou linge.',
  },
  weather: {
    code: 'weather',
    title: 'Influence de la pluie à vérifier',
    description: 'Les rares hausses coïncident avec des jours de pluie. C’est un indice de contexte à comparer avec une période sèche, pas la preuve d’une infiltration.',
  },
  'air-vapor': {
    code: 'air-vapor',
    title: 'Air humide persistant — ventilation à contrôler',
    description: 'Les dépassements reviennent aussi hors activité. Le renouvellement d’air est la première piste à vérifier.',
  },
  condensation: {
    code: 'condensation',
    title: 'Condensation possible',
    description: 'Les mesures et les signes déclarés sont compatibles avec de la condensation, sans suffire à identifier seuls la cause.',
  },
  'water-building': {
    code: 'water-building',
    title: 'Entrée d’eau ou bâti à vérifier',
    description: 'Les signes localisés ou leur lien avec la pluie demandent une recherche technique plutôt qu’un simple traitement de l’air.',
  },
  'hidden-local': {
    code: 'hidden-local',
    title: 'Humidité locale à rechercher',
    description: 'L’air moyen paraît correct, mais l’odeur ou les traces localisées peuvent signaler un support humide ou une zone froide cachée.',
  },
  'mold-widespread': {
    code: 'mold-widespread',
    title: 'Moisissures sur plusieurs zones — intervention à organiser',
    description: 'La présence déclarée sur plusieurs zones justifie une recherche de cause et un traitement adapté, même si l’humidité moyenne de l’air paraît correcte.',
  },
  indeterminate: {
    code: 'indeterminate',
    title: 'Résultat à compléter',
    description: 'Les données ne permettent pas de dégager une piste principale suffisamment cohérente.',
  },
};

const ROOM_LABELS = {
  chambre: 'chambre', salon: 'salon / séjour', 'salle-bain': 'salle de bain',
  cuisine: 'cuisine', buanderie: 'buanderie', cave: 'cave / sous-sol', autre: 'autre pièce',
};

function ventilationCheckFor(roomType, ventilation) {
  const isExtractedRoom = ['salle-bain', 'cuisine', 'buanderie'].includes(roomType);
  const device = isExtractedRoom ? 'la bouche d’extraction' : 'les entrées d’air attendues';
  if (ventilation === 'yes') return `Vous avez déclaré ${device} présente(s), ouverte(s) et propre(s) : vérifiez maintenant le fonctionnement réel et l’absence d’obstruction.`;
  if (ventilation === 'no') return `Rendez ${device} présente(s), ouverte(s) et propre(s), puis vérifiez l’évolution pendant trois jours comparables.`;
  if (ventilation === 'unknown') return `Repérez ${device} et contrôlez sa présence, son ouverture et sa propreté avant de poursuivre l’interprétation.`;
  return `Confirmez si ${device} devrait équiper cette pièce ; « non applicable » ne permet pas d’écarter un renouvellement d’air insuffisant.`;
}

function actionsFor(code, roomType, ventilation) {
  const actions = {
    reassuring: [
      'Aucun achat nécessaire sur la base de ce suivi.',
      'Conservez le compte rendu et refaites une semaine de mesures seulement si un signe apparaît ou si la saison change fortement.',
      'Agissez sans attendre si une fuite, un mur mouillé ou des moisissures étendues apparaissent.',
    ],
    'high-comfort-zone': [
      ventilationCheckFor(roomType, ventilation),
      'Surveillez l’évolution sans chercher à faire baisser un chiffre isolé : comparez surtout des relevés pris à température et horaires proches.',
      'Si les valeurs dépassent régulièrement 60 % ou si une odeur, une trace ou de la condensation apparaît, recherchez alors la cause locale avant tout achat.',
    ],
    'activity-peaks': [
      'Après douche, cuisson ou séchage du linge, utilisez immédiatement l’extraction ou aérez jusqu’à disparition de la vapeur.',
      'Refaites un relevé 60 minutes après cette activité : l’humidité doit redescendre vers la valeur habituelle de la pièce.',
      'N’achetez pas de déshumidificateur si les valeurs redescendent correctement entre les activités.',
    ],
    weather: [
      'Ajoutez deux jours sans pluie, avec des relevés aux mêmes heures et avant d’aérer, puis comparez-les aux jours pluvieux.',
      'Si une trace apparaît ou s’aggrave précisément après la pluie, photographiez-la, datez-la et faites vérifier le bâti.',
      'Ne concluez pas à une infiltration sur les pourcentages seuls : la météo extérieure peut aussi influencer l’air intérieur.',
    ],
    'air-vapor': [
      ventilationCheckFor(roomType, ventilation),
      'Pendant 3 jours comparables, limitez linge intérieur et vapeur puis observez si les valeurs restent supérieures à 60 %.',
      'Si elles restent élevées malgré ces vérifications, faites contrôler la ventilation avant d’acheter un appareil.',
    ],
    condensation: [
      'Repérez la surface concernée : vitre, angle, mur extérieur ou zone derrière un meuble.',
      'Mesurez sa température et utilisez le calculateur de point de rosée du site pour vérifier la piste condensation.',
      'Améliorez l’extraction de vapeur et laissez 5 à 10 cm entre le meuble et le mur froid.',
    ],
    'water-building': [
      'Ne masquez pas la trace avec peinture, parfum ou absorbeur seul.',
      'Photographiez et datez la zone, puis vérifiez fuite, joint, toiture, façade ou canalisation selon son emplacement.',
      'Si la zone est mouillée maintenant, s’étend ou revient après pluie, contactez rapidement un professionnel du bâtiment et votre assurance selon la situation.',
    ],
    'hidden-local': [
      'Inspectez derrière meubles, plinthes, revêtements et dans les angles proches de la zone signalée.',
      'Comparez l’air de cette zone avec le centre de la pièce, dans les mêmes conditions.',
      'Si l’odeur ou les traces reviennent malgré un air normal, demandez un contrôle du support ou du bâti.',
    ],
    'mold-widespread': [
      'Photographiez les zones et évitez de brosser à sec ou de masquer les traces.',
      'Faites rechercher rapidement la source d’humidité et l’étendue réelle avant de refaire les finitions.',
      'Si une personne fragile présente des symptômes, demandez aussi un avis médical.',
    ],
    indeterminate: [
      'Vérifiez que les 14 mesures ont été prises au même endroit et avant d’aérer.',
      'Refaites uniquement les contrôles indiqués comme inconnus ou contradictoires.',
      'En présence de signes visibles persistants, demandez un avis professionnel plutôt que de déduire une cause des pourcentages seuls.',
    ],
  };
  return actions[code];
}

export function analyzeHumidityWeek(input) {
  const readings = Array.isArray(input?.readings) ? input.readings : [];
  const completeReadings = readings.filter(isCompleteReading);
  if (completeReadings.length !== 14) {
    return {
      status: 'incomplete',
      missingReadings: Math.max(0, 14 - completeReadings.length),
      message: 'Le compte rendu complet nécessite 14 relevés : matin et soir pendant 7 jours.',
    };
  }

  const expectedSlots = Array.from({ length: 7 }, (_, index) => [
    `${index + 1}-morning`, `${index + 1}-evening`,
  ]).flat();
  const actualSlots = new Set(completeReadings.map((reading) => `${Number(reading.day)}-${reading.period}`));
  const missingSlots = expectedSlots.filter((slot) => !actualSlots.has(slot));
  if (actualSlots.size !== 14 || missingSlots.length > 0) {
    const labels = missingSlots.map((slot) => {
      const [day, period] = slot.split('-');
      return `jour ${day} ${period === 'morning' ? 'matin' : 'soir'}`;
    });
    return {
      status: 'incomplete',
      missingReadings: missingSlots.length,
      message: `Chaque créneau doit être renseigné une seule fois. Manquant : ${labels.join(', ')}.`,
    };
  }

  const ordered = [...completeReadings].sort((a, b) => Number(a.day) - Number(b.day)
    || (a.period === 'morning' ? -1 : 1));
  const rhs = ordered.map((reading) => Number(reading.rh));
  const temperatures = ordered.map((reading) => Number(reading.temp));
  const morning = ordered.filter((reading) => reading.period === 'morning').map((reading) => Number(reading.rh));
  const evening = ordered.filter((reading) => reading.period === 'evening').map((reading) => Number(reading.rh));
  const countAbove60 = rhs.filter((value) => value > 60).length;
  const countAtLeast70 = rhs.filter((value) => value >= 70).length;
  const countHighComfort = rhs.filter((value) => value >= 55 && value <= 60).length;
  const contextMap = readingContextMap(input.contexts);
  const activityDays = [...contextMap.keys()].filter((day) => contextHas(contextMap, day, 'activity'));
  const rainDays = [...contextMap.keys()].filter((day) => contextHas(contextMap, day, 'rain'));
  const activityHighDays = activityDays.filter((day) => dayHasHighReading(ordered, day)).length;
  const activityHighReadings = ordered.filter((reading) => contextHas(contextMap, reading.day, 'activity') && Number(reading.rh) > 60).length;
  const highOutsideActivity = ordered.filter((reading) => !contextHas(contextMap, reading.day, 'activity') && Number(reading.rh) > 60).length;
  const rainHighDays = rainDays.filter((day) => dayHasHighReading(ordered, day)).length;
  const rainHighReadings = ordered.filter((reading) => contextHas(contextMap, reading.day, 'rain') && Number(reading.rh) > 60).length;
  const otherDays = [...contextMap.keys()].filter((day) => contextHas(contextMap, day, 'other')).length;
  const signs = input.signs || {};
  const hasAnySign = Object.values(signs).some(Boolean);
  const validAnswers = ['yes', 'no', 'unknown', 'na'];
  if (!validAnswers.includes(input.rainWorse) || !validAnswers.includes(input.ventilation)
    || !['none', 'local', 'multiple'].includes(input.scope)) {
    return {
      status: 'incomplete-context',
      message: 'Répondez aux trois questions de bilan après le dernier relevé du jour 7.',
    };
  }
  if (signs.moldRecurring && !signs.mold) {
    return {
      status: 'incomplete-context',
      message: 'Réponse contradictoire : une récidive de moisissure nécessite aussi de cocher « Moisissure visible ».',
    };
  }
  if ((hasAnySign && input.scope === 'none') || (!hasAnySign && input.scope !== 'none')) {
    return {
      status: 'incomplete-context',
      message: 'Réponse contradictoire : accordez les signes cochés avec leur portée (aucun, une zone ou plusieurs zones).',
    };
  }
  const technicalWater = Boolean(signs.wetWall || signs.blistering || signs.salts || input.rainWorse === 'yes');
  const localizedHidden = input.scope === 'local' && Boolean(signs.odor || signs.mold) && !technicalWater;

  const summary = {
    averageRh: round1(mean(rhs)),
    minRh: Math.min(...rhs),
    maxRh: Math.max(...rhs),
    countAbove60,
    countAtLeast70,
    countHighComfort,
    countInRange: rhs.filter((value) => value >= 40 && value <= 60).length,
    morningAverageRh: round1(mean(morning)),
    eveningAverageRh: round1(mean(evening)),
    averageTemperature: round1(mean(temperatures)),
    minTemperature: Math.min(...temperatures),
    maxTemperature: Math.max(...temperatures),
    temperatureRange: round1(Math.max(...temperatures) - Math.min(...temperatures)),
    longestHighStreak: longestStreak(rhs, (value) => value > 60),
    activityHighDays,
    rainHighDays,
  };

  let primaryCode = 'indeterminate';
  const secondaryCodes = [];
  const evidence = [
    `Pièce suivie : ${ROOM_LABELS[input.roomType] || ROOM_LABELS.autre}.`,
    `${countAbove60} relevés sur 14 au-dessus de 60 % ; ${countAtLeast70} à 70 % ou plus.`,
    `${countHighComfort} relevés sur 14 entre 55 et 60 % (zone haute du repère 40–60 %).`,
    `Humidité moyenne ${summary.averageRh.toFixed(1).replace('.', ',')} % ; minimum ${summary.minRh} % ; maximum ${summary.maxRh} %.`,
  ];
  if (activityHighReadings > 0) evidence.push(`${activityHighReadings} relevé(s) élevé(s) ont été mesurés lors de journées où une activité produisant de la vapeur a été signalée ; cela ne prouve pas qu’elle en est la seule cause.`);
  if (rainHighReadings > 0) evidence.push(`${rainHighReadings} relevé(s) élevé(s) ont été mesurés lors de jours de pluie ; cette association doit être comparée à des jours secs.`);
  if (otherDays > 0) evidence.push(`${otherDays} journée avec un autre changement a été signalée ; elle est conservée comme contexte sans lui attribuer une cause.`);

  if (signs.mold && (input.scope === 'multiple' || signs.moldRecurring)) {
    primaryCode = 'mold-widespread';
    evidence.push(signs.moldRecurring
      ? 'La moisissure a été déclarée comme réapparue après nettoyage : ce constat prime sur la moyenne de l’air.'
      : 'Des moisissures ont été déclarées sur plusieurs zones : ce constat prime sur la moyenne de l’air.');
  } else if (technicalWater) {
    primaryCode = 'water-building';
    if (input.rainWorse === 'yes') evidence.push('Une aggravation après la pluie a été déclarée pendant la semaine.');
    if (signs.wetWall) evidence.push('Un mur actuellement mouillé a été déclaré : ce signe prime sur les pourcentages.');
    if (countAbove60 >= 4) secondaryCodes.push('air-vapor');
  } else if (localizedHidden && summary.averageRh <= 60) {
    primaryCode = 'hidden-local';
    evidence.push('Des signes localisés sont présents malgré une humidité moyenne qui ne dépasse pas 60 %.');
  } else if (signs.condensation && (summary.morningAverageRh > summary.eveningAverageRh || countAbove60 >= 3)) {
    primaryCode = 'condensation';
    evidence.push('De la condensation a été observée et les mesures montrent des périodes plus humides.');
    if (input.ventilation === 'no') secondaryCodes.push('air-vapor');
  } else if (countAbove60 >= 1 && countAbove60 <= 3 && countAtLeast70 === 0
    && rainHighReadings >= Math.max(1, countAbove60 - 1)) {
    primaryCode = 'weather';
    if (activityHighReadings > 0) secondaryCodes.push('activity-peaks');
  } else if (countAbove60 >= 1 && countAbove60 <= 3 && countAtLeast70 === 0
    && activityHighReadings >= Math.max(1, countAbove60 - 1) && highOutsideActivity <= 1) {
    primaryCode = 'activity-peaks';
    if (rainHighReadings > 0) secondaryCodes.push('weather');
  } else if ((countAbove60 >= 4 || countAtLeast70 >= 2)
    && (highOutsideActivity >= 2 || summary.longestHighStreak >= 3)) {
    primaryCode = 'air-vapor';
    evidence.push(`Les dépassements persistent hors activité ou sur ${summary.longestHighStreak} relevés consécutifs.`);
    if (input.ventilation === 'no') evidence.push('Les entrées d’air ou l’extraction ont été déclarées absentes, fermées ou encrassées.');
    if (signs.condensation) secondaryCodes.push('condensation');
  } else if (countAbove60 === 0 && countHighComfort >= 7 && !hasAnySign
    && input.rainWorse !== 'yes' && input.ventilation !== 'no') {
    primaryCode = 'high-comfort-zone';
    evidence.push('La répétition des valeurs proches de 60 % justifie une surveillance, même sans dépassement du seuil.');
  } else if (countAbove60 <= 2 && countAtLeast70 === 0 && !hasAnySign
    && input.rainWorse !== 'yes' && input.ventilation !== 'no') {
    primaryCode = 'reassuring';
    evidence.push('Aucun signe visible n’a été déclaré et les dépassements sont absents ou rares.');
  } else if (localizedHidden) {
    primaryCode = 'hidden-local';
    evidence.push('Les signes restent concentrés sur une zone précise.');
  }

  const temperatureNote = summary.temperatureRange >= 3
    ? `La température a varié de ${summary.temperatureRange.toFixed(1).replace('.', ',')} °C. Interprétez les écarts d’humidité relative avec prudence : comparez surtout les relevés pris dans des conditions proches.`
    : `La température est restée assez comparable (amplitude ${summary.temperatureRange.toFixed(1).replace('.', ',')} °C), ce qui rend la comparaison des pourcentages plus fiable.`;

  const primary = PROFILES[primaryCode];
  const secondary = [...new Set(secondaryCodes)]
    .filter((code) => code !== primaryCode)
    .map((code) => PROFILES[code]);
  const alert = signs.wetWall
    ? { level: 'urgent', message: 'Mur mouillé déclaré : n’attendez pas une nouvelle semaine de mesures.' }
    : (signs.mold && (input.scope === 'multiple' || signs.moldRecurring))
      ? { level: 'urgent', message: signs.moldRecurring ? 'Moisissure récidivante déclarée : faites contrôler la zone sans attendre.' : 'Moisissures déclarées sur plusieurs zones : faites contrôler sans attendre.' }
      : (input.rainWorse === 'yes' || signs.blistering || signs.salts)
        ? { level: 'check', message: 'Indice lié au bâti : documentez la zone et faites-la vérifier si elle persiste ou s’aggrave.' }
        : { level: 'none', message: '' };

  return {
    status: 'complete',
    summary,
    primary,
    secondary,
    evidence,
    actions: actionsFor(primaryCode, input.roomType, input.ventilation),
    alert,
    temperatureNote,
  };
}
