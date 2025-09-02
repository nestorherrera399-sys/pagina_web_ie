document.addEventListener("DOMContentLoaded", function () {
  const chatbotBody = document.getElementById("chatbot-body");
  const chatbotInput = document.getElementById("chatbot-input");
  const sendBtn = document.getElementById("chatbot-send-btn"); // Asegúrate que tienes este botón en tu HTML


  // Base de preguntas y respuestas
  const respuestas = [
    { pregunta: "hola", respuesta: "Hola, ¿en qué te puedo ayudar el día de hoy?" },
    { pregunta: "francisco bolognesi", respuesta: "Francisco Bolognesi fue un héroe nacional peruano, conocido por su valentía y sacrificio en la defensa del país durante la Guerra del Pacífico." },
    { pregunta: "por qué se llama francisco bolognesi", respuesta: "El colegio lleva el nombre de Francisco Bolognesi en honor a su legado y valentía como símbolo de patriotismo para inspirar a los estudiantes." },
    { pregunta: "quién creó esta página", respuesta: "Esta página fue creada por el alumno de Senati: Nestor Herrera Zevallos." },
    { pregunta: "quién fue el creador", respuesta: "El creador fue el alumno de Senati: Nestor Herrera Zevallos." },
    { pregunta: "qué es esta página", respuesta: "Esta es la página oficial de la IE Francisco Bolognesi, donde encontrarás información sobre la institución, servicios, noticias, testimonios y más." },

    { pregunta: "historia del colegio", respuesta: "La IE Francisco Bolognesi fue fundada para brindar educación integral a la comunidad, destacándose por su compromiso con la formación académica y valores cívicos." },
    { pregunta: "misión", respuesta: "Nuestra misión es formar estudiantes íntegros, críticos y comprometidos con la sociedad, capaces de enfrentar los retos del mundo con valores y conocimientos sólidos." },
    { pregunta: "visión", respuesta: "Nuestra visión es ser una institución educativa líder en la región, reconocida por su excelencia académica, innovación pedagógica y formación en valores." },
    { pregunta: "valores", respuesta: "Promovemos valores como la honestidad, respeto, responsabilidad, solidaridad y compromiso social, que son la base de nuestra comunidad educativa." },

    { pregunta: "qué hace el área de psicología", respuesta: "Ofrece apoyo emocional, asesoramiento psicológico, prevención de bullying, charlas, talleres y acompañamiento a estudiantes." },
    { pregunta: "puedo hablar con el psicólogo", respuesta: "Sí, puedes acercarte a la Oficina de Psicología en el horario de atención o comunicarte con un docente para solicitar ayuda." },
    { pregunta: "dónde está la oficina de psicología", respuesta: "Está ubicada junto a la Dirección de la institución." },
    { pregunta: "qué hacer si me siento estresado", respuesta: "Puedes acudir al área de Psicología donde te brindarán orientación y estrategias para manejar el estrés." },
    { pregunta: "qué hacer si un amigo está triste", respuesta: "Escúchalo con empatía y sugiérele que hable con el psicólogo escolar para recibir apoyo profesional." },
    { pregunta: "hay talleres emocionales", respuesta: "Sí, se ofrecen talleres sobre habilidades socioemocionales, prevención del bullying y desarrollo personal." },
    { pregunta: "qué hacer ante el bullying", respuesta: "Debes informarlo a un docente o al área de psicología. No estás solo, podemos ayudarte." },
    { pregunta: "puedo hablar de mis problemas familiares", respuesta: "Sí, el área de Psicología está para escucharte y orientarte con total confidencialidad." },
    { pregunta: "pueden ayudarme si tengo ansiedad", respuesta: "Sí, se brindan sesiones y estrategias para el manejo de la ansiedad escolar y personal." },
    { pregunta: "hay apoyo para los padres", respuesta: "Sí, ofrecemos guías, talleres y orientación personalizada para las familias." },

    { pregunta: "cuáles son los mejores libros para aprender", respuesta: "Te recomendamos libros como 'El Principito', 'Cuentos de valores', 'Enciclopedia Escolar' y libros de lectura sugeridos por el docente." },
    { pregunta: "dónde puedo encontrar cuentos", respuesta: "Puedes revisar nuestra sección de biblioteca o consultar con tu profesor de comunicación." },
    { pregunta: "qué cuentos recomiendas", respuesta: "Cuentos como 'Los zapatos del abuelo', 'La vaca', y 'El árbol generoso' son excelentes para reflexionar y aprender valores." },
    { pregunta: "hay biblioteca en el colegio", respuesta: "Sí, contamos con una biblioteca equipada para todos los niveles educativos." },
    { pregunta: "puedo llevar libros a casa", respuesta: "Sí, puedes solicitar el préstamo con tu carnet escolar, según las normas de la biblioteca." },
    { pregunta: "hay libros de ayuda emocional", respuesta: "Sí, contamos con material sobre autoestima, resolución de conflictos y habilidades sociales." },
    { pregunta: "puedo leer en el recreo", respuesta: "Sí, la biblioteca está disponible en ciertos horarios también durante los recreos." },
    { pregunta: "recomiendas leer cuentos para dormir", respuesta: "Sí, leer cuentos antes de dormir ayuda a desarrollar la imaginación y mejorar el descanso." },
    { pregunta: "cómo me ayuda leer cuentos", respuesta: "Leer cuentos mejora tu comprensión, creatividad, vocabulario y desarrollo emocional." },
    { pregunta: "puedo escribir mi propio cuento", respuesta: "¡Claro! Incluso puedes compartirlo con tus docentes o publicarlo en la cartelera escolar." },

    { pregunta: "qué días importantes celebramos", respuesta: "Celebramos fechas como el Día del Logro, Día del Maestro, Aniversario del colegio, Fiestas Patrias, entre otros." },
    { pregunta: "cuándo es el día del logro", respuesta: "El Día del Logro se realiza dos veces al año para mostrar los avances académicos de los estudiantes." },
    { pregunta: "qué actividades hacen en fiestas patrias", respuesta: "Desfiles, concursos de danzas, exposiciones culturales y presentaciones artísticas." },
    { pregunta: "hay concursos de arte o danza", respuesta: "Sí, durante el año organizamos concursos de arte, danza, canto y talentos escolares." },
    { pregunta: "cómo participo en actividades culturales", respuesta: "Puedes inscribirte a través de tus docentes o en la coordinación del área cultural." },
    { pregunta: "hay talleres multimedia", respuesta: "Sí, el área de multimedia apoya en la producción de material audiovisual para los eventos escolares." },
    { pregunta: "quién organiza las actividades", respuesta: "Las actividades son organizadas por los docentes junto con el equipo directivo y apoyo estudiantil." },
    { pregunta: "puedo presentar un video o proyecto", respuesta: "Sí, puedes coordinar con tus docentes para presentar materiales en fechas importantes." },
    { pregunta: "cómo me entero de los eventos", respuesta: "Revisando la sección 'Noticias' en la web o preguntando a tus docentes." },
    { pregunta: "hay feria escolar", respuesta: "Sí, organizamos ferias escolares donde los estudiantes presentan proyectos de ciencia, arte y más." },

    { pregunta: "cómo me inscribo", respuesta: "Puedes inscribirte desde la sección 'Inscripción' presentando los requisitos como DNI, certificado de estudios, y partida de nacimiento." },
    { pregunta: "qué documentos necesito para inscribirme", respuesta: "DNI del estudiante, partida de nacimiento, libreta anterior y llenar el formulario en línea." },
    { pregunta: "hay vacantes disponibles", respuesta: "Sí, pero están sujetas a disponibilidad. Revisa la sección 'Admisión'." },
    { pregunta: "dónde están ubicados", respuesta: "Estamos ubicados en la ciudad de Ilo, puedes ver la dirección exacta en la sección 'Contacto'." },
    { pregunta: "cuál es el correo de contacto", respuesta: "Puedes escribirnos al correo contacto@iefbolognesi.edu.pe" },
    { pregunta: "hay número de teléfono", respuesta: "Sí, puedes llamarnos al (01) 234-5678 para más información." },
    { pregunta: "qué servicios ofrecen", respuesta: "Educación básica, orientación psicológica, biblioteca, talleres y acompañamiento a los estudiantes." },
    { pregunta: "puedo recibir apoyo escolar", respuesta: "Sí, contamos con asesoría y refuerzo en diversas materias según lo requiera el estudiante." },
    { pregunta: "tienen redes sociales", respuesta: "Sí, estamos en Facebook: https://www.facebook.com/profile.php?id=61551563597462" },
    { pregunta: "dónde veo las noticias", respuesta: "Revisa la sección 'Noticias' donde actualizamos eventos y avisos importantes." },

    { pregunta: "necesito ayuda", respuesta: "¡Estoy aquí para ayudarte! Pregunta lo que necesites sobre la IE Francisco Bolognesi." },
    { pregunta: "eres un asistente", respuesta: "Sí, soy un asistente virtual diseñado para responder tus preguntas sobre la institución." },
    { pregunta: "en qué puedes ayudarme", respuesta: "Puedo ayudarte con información sobre inscripción, eventos, servicios, contacto, psicología y más." },
    { pregunta: "puedo confiar en ti", respuesta: "Sí, mi información está basada en el contenido oficial de la institución educativa." },
    { pregunta: "me puedes recomendar algo", respuesta: "Claro, dime si buscas recomendaciones de libros, actividades o cómo resolver alguna duda escolar." },
    { pregunta: "qué secciones hay en la web", respuesta: "Tenemos Nosotros, Escolaridad, Recursos, Noticias, Testimonios, Trámites y Admisión." },
    { pregunta: "qué es la sección escolaridad", respuesta: "Allí encontrarás información sobre los niveles educativos, docentes y áreas académicas." },
    { pregunta: "qué es la sección recursos", respuesta: "Reúne documentos y materiales útiles como guías, prevención del bullying, manejo del estrés y más." },
    { pregunta: "qué es la sección testimonios", respuesta: "Es un espacio para que estudiantes y padres compartan sus experiencias con la institución." },
    { pregunta: "quién responde este chat", respuesta: "Soy un asistente automático basado en JavaScript programado para ayudarte con todo lo que necesites sobre el colegio." },

    { pregunta: "qué es java", respuesta: "Java es un lenguaje de programación ampliamente usado para desarrollar aplicaciones, desde móviles hasta sistemas empresariales." },
    { pregunta: "que es java", respuesta: "Java es un lenguaje de programación ampliamente usado para desarrollar aplicaciones, desde móviles hasta sistemas empresariales." },
    { pregunta: "java", respuesta: "Java es un lenguaje de programación popular y robusto, utilizado tanto en la web como en aplicaciones móviles." },
    { pregunta: "qué es programación", respuesta: "La programación es el proceso de crear instrucciones para que un computador realice tareas específicas, usando lenguajes como Java, Python o JavaScript." },
    { pregunta: "qué es senati", respuesta: "Senati es una institución educativa técnica peruana que ofrece formación profesional en diversas áreas tecnológicas e industriales." },
    { pregunta: "quién es nestor herrera zevallos", respuesta: "Es el alumno de Senati que creó y desarrolló esta página web como parte de su formación profesional en Ingeniería de Software con Inteligencia Artificial." },
    { pregunta: "qué es inteligencia artificial", respuesta: "La inteligencia artificial es una rama de la informática que crea sistemas capaces de realizar tareas que normalmente requieren inteligencia humana, como aprender, razonar o resolver problemas." }
  ];

  const fuse = new Fuse(respuestas, {
    keys: ["pregunta"],
    threshold: 0.3,
  });

  const saludos = ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches"];
  const despedidas = ["adios", "hasta luego", "nos vemos", "chao"];

  let historial = JSON.parse(localStorage.getItem("chatHistorial") || "[]");

  // Cargar historial en pantalla
  historial.forEach((msg) => {
    chatbotBody.insertAdjacentHTML(
      "beforeend",
      `<div class="${msg.who}-message"><strong>${msg.who === "user" ? "Tú" : "Bot"}:</strong> ${msg.text}</div>`
    );
  });
  chatbotBody.scrollTop = chatbotBody.scrollHeight;

  function scrollBottom() {
    chatbotBody.scrollTo(0, chatbotBody.scrollHeight);
  }

  function guardarEnHistorial(who, text) {
    historial.push({ who, text });
    localStorage.setItem("chatHistorial", JSON.stringify(historial));
  }

  function getBotResponse(input) {
    input = input.toLowerCase();
    if (saludos.some((s) => input.includes(s))) {
      return "¡Hola! ¿En qué puedo ayudarte?";
    }
    if (despedidas.some((d) => input.includes(d))) {
      return "¡Hasta pronto! Cuídate.";
    }
    if (input.includes("gracias")) {
      return "¡De nada! Estoy para ayudarte.";
    }
    if (input === "si" || input === "sí") {
      return "Perfecto, dime más.";
    }
    if (input === "no") {
      return "Entiendo. Si necesitas algo, dime.";
    }

    const resultado = fuse.search(input);
    if (resultado.length > 0) {
      return resultado[0].item.respuesta;
    } else {
      const sugerencias = [
        "¿Quieres saber sobre la inscripción?",
        "Puedes preguntar sobre los servicios del colegio.",
        "Consulta fechas importantes como el Día del Logro.",
      ];
      const aleatorias = sugerencias.sort(() => 0.5 - Math.random()).slice(0, 3);
      return (
        "Lo siento, aún no entiendo eso. Puedes intentar:<br>" +
        "<ul style='margin-top: 0.5rem;'>" +
        aleatorias.map((s) => `<li>${s}</li>`).join("") +
        "</ul>"
      );
    }
  }

  function enviarMensaje() {
    const pregunta = chatbotInput.value.trim();
    if (pregunta === "") return;

    chatbotBody.insertAdjacentHTML(
      "beforeend",
      `<div class="user-message"><strong>Tú:</strong> ${pregunta}</div>`
    );
    guardarEnHistorial("user", pregunta);

    const respuesta = getBotResponse(pregunta);
    chatbotBody.insertAdjacentHTML(
      "beforeend",
      `<div class="bot-message"><strong>Bot:</strong> ${respuesta}</div>`
    );
    guardarEnHistorial("bot", respuesta);

    chatbotInput.value = "";
    chatbotInput.focus();
    scrollBottom();
  }

  chatbotInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      enviarMensaje();
    }
  });

  if(sendBtn) {
    sendBtn.addEventListener("click", enviarMensaje);
  }
});