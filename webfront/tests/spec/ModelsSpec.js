describe("Avame Models", function() {

  describe("Notice", function() {
    it("Can be created with default values for its attributes.", function() {
      var script = new ava.models.Script();
      expect(script.get('title')).toBe('');
    });
  });

  describe("Job", function() {
    it("Can be created with default values for its attributes.", function() {
      var job = new ava.models.Job();
      expect(job.get('name')).toBe('');
      expect(job.get('st')).toBe('');
    });
  });

  describe("Log", function() {
    it("Can be created with default values for its attributes.", function() {
      var log = new ava.models.Log();
      expect(log.get('ts')).toBe(0);
      expect(log.get('lvl')).toBe(20);
      expect(log.get('lvl_name')).toBe('INFO');
      expect(log.get('msg')).toBe('');
    });
  });

  describe("Script", function() {
    it("Can be created with default values for its attributes.", function() {
      var script = new ava.models.Script();
      expect(script.get('title')).toBe('');
      expect(script.get('content')).toBe('');
    });
  });

  describe("Session", function() {
    it("Can be created with default values for its attributes.", function() {
      var session = new ava.models.Session();
      expect(session.get('token')).toBeNull();
    });
  });

});
